from django.http import Http404, HttpResponse
from django.conf import settings
from django.template.loader import render_to_string

import json

from controllers import ImagePath
from utils import process_image


def upload(request):
    if not request.method == 'POST':
        raise Http404

    response_data = {}
    if request.is_ajax():
        if request.FILES:
            image = request.FILES.values()[0]
            path = process_image(image, request.user.id)
            try:
                preview_size = request.POST['preview_size']
            except KeyError:
                preview_size = '64'
            response_data['status'] = True
            response_data['imagePath'] = path
            response_data['thumbnail'] = render_to_string('files_widget/includes/thumbnail.html',
                                                          {'MEDIA_URL': settings.MEDIA_URL,
                                                           'STATIC_URL': settings.STATIC_URL,
                                                           'preview_size': preview_size})
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        else:
            response_data['status'] = False
            response_data['message'] = "We're sorry, but something went wrong."
            return HttpResponse(json.dumps(response_data), content_type='application/json')


def thumbnail_url(request):
    if not 'img' in request.GET or not 'preview_size' in request.GET:
        raise Http404
    
    thumbnail_url = ImagePath(request.GET['img']).thumbnail(request.GET['preview_size']).url
    return HttpResponse(thumbnail_url)
