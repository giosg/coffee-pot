"""
Contains picture recognizion related view classes.
"""
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from webcam.models import Picture
from .forms import PictureLabelizerForm
from .forms import PictureLeftLabelizerForm, PictureRightLabelizerForm


def labelize_picture_left_sides(request):
    """
    Shows the HTML page for labelizing unlabeled left-sides of pictures.
    """
    form_set = modelformset_factory(Picture, form=PictureLeftLabelizerForm, extra=0)
    pics = Picture.objects.filter(left_label__isnull=True).order_by('-created_at')
    if request.method == 'POST':
        # HACK: pics[:100] is enough Pictures to contain all Pictures for which labels were submitted, but not too many to be slow to query
        # We get new Picture every minute from cronjob, so one can spend 50 minutes labeling 50 pictures before this fails, i.e. returns 500
        formset = form_set(request.POST, request.FILES, queryset=pics[:100])
        if formset.is_valid():
            formset.save()
            return redirect('left_labelizer')
    else:
        formset = form_set(queryset=pics[:50])
    return render(request, 'labelizer.html', {
        'labelizer_side': 'left',
        'formset': formset,
        'unlabeled_count': Picture.objects.filter(left_label__isnull=True).count(),
    })


def labelize_picture_right_sides(request):
    """
    Shows the HTML page for labelizing unlabeled right-sides of pictures.
    """
    form_set = modelformset_factory(Picture, form=PictureRightLabelizerForm, extra=0)
    pics = Picture.objects.filter(right_label__isnull=True).order_by('-created_at')
    if request.method == 'POST':
        formset = form_set(request.POST, request.FILES, queryset=pics[:100])
        if formset.is_valid():
            formset.save()
            return redirect('right_labelizer')
    else:
        formset = form_set(queryset=pics[:50])
    return render(request, 'labelizer.html', {
        'labelizer_side': 'right',
        'formset': formset,
        'unlabeled_count': Picture.objects.filter(right_label__isnull=True).count(),
    })


def labelize_pictures(request):
    """
    Shows the HTML page for labelizing unlabeled pictures.
    """
    form_set = modelformset_factory(Picture, form=PictureLabelizerForm, extra=0)
    pics = Picture.objects.filter(label__isnull=True).order_by('-created_at')
    if request.method == 'POST':
        formset = form_set(request.POST, request.FILES, queryset=pics[:100])
        if formset.is_valid():
            formset.save()
            return redirect('labelizer')
    else:
        formset = form_set(queryset=pics[:50])
    return render(request, 'labelizer.html', {
        'formset': formset,
        'unlabeled_count': Picture.objects.filter(label__isnull=True).count(),
    })
