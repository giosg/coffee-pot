"""barista URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from coffeestatus.views import CoffeeStatusView
from recognition.views import LabelizerView
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', CoffeeStatusView.as_view()),
    url(r'^labelizer/?$', LabelizerView.as_view()),
    url(r'^admin/', admin.site.urls),
]
# Serve static files in development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Serve media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
