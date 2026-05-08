from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'masterfile', views.MasterFileModelViewSet,
                basename='masterfile')
router.register(r'chunkedfile', views.ChunkedFileModelViewSet,
                basename='chunkedfile')

urlpatterns = [
    path('chunkedfile/last-chunk/', views.ChunkedFileModelViewSet.as_view({'get': 'last_chunk'}), name='chunkedfile-last-chunk'),
    path('chunkedfile/merge-chunks/', views.ChunkedFileModelViewSet.as_view({'get': 'merge_chunks'}), name='chunkedfile-merge-chunks'),
    path('chunkedfile/download/', views.ChunkedFileModelViewSet.as_view({'get': 'download_file'}), name='chunkedfile-download'),
]
urlpatterns += router.urls
