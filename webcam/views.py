import csv
from django.http import StreamingHttpResponse
from webcam.models import Picture
from django.utils.dateparse import parse_datetime
from django.http import HttpResponse


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def dump_labeled_pics(request):
    """A view that streams a labeled pictures as a CSV file."""
    since = request.GET.get('since', '1970-01-01T00:00:00.000Z')
    since_dt = None
    try:
        since_dt = parse_datetime(since)
        if not since_dt:
            raise ValueError('\'since\' is not a valid date')
    except ValueError as ex:
        return HttpResponse(ex.message, status=400)
    pics = Picture.objects.filter(left_label__isnull=False, right_label__isnull=False, created_at__gt=since_dt) \
        .order_by('created_at')
    rows = ([pic.image.url, pic.left_label_id, pic.right_label_id] for pic in pics.iterator())
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="labeled_pics.csv"'
    return response
