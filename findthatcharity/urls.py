"""findthatcharity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

import addtocsv.views
import charity.urls
import ftc.urls
import ftc.views
import reconcile.urls
from api.endpoints import api

urlpatterns = [
    path("admin/", admin.site.urls, name="about"),
    path("", ftc.views.index, name="index"),
    path("about", ftc.views.about, name="about"),
    path("adddata/", addtocsv.views.index, name="csvtool"),
    path("api/v1/", api.urls),
    path("orgid/", include(ftc.urls)),
    path("charity/", include(charity.urls)),
    path("reconcile/", include(reconcile.urls)),
    path("reconcile", reconcile.views.index, {"orgtype": "registered-charity"}),
]
