from django.utils.text import slugify
try:
    from django.utils.module_loading import import_string  # Django >= 1.7
except ImportError:
    from django.utils.module_loading import import_by_path as import_string  # Django == 1.6
from django.core.files.storage import default_storage

try:
    from io import BytesIO as BufferIO
except ImportError:
    from cStringIO import StringIO as BufferIO
from os import path
try:
    from PIL import Image
except ImportError:
    import Image
from hashlib import md5

from .settings import FILES_DIR, IMAGE_MAX_SIZE, HASH_NAMES


def get_name(filename):
    base, ext = path.splitext(filename)
    if HASH_NAMES:
        return md5(base).hexdigest()[0:10] + ext
    return slugify(base) + ext


def get_path(user, filename):
    return '{}/{}/{}'.format(FILES_DIR, user, get_name(filename))


def resize_image(in_file, out_file):
    img = Image.open(in_file)
    img.thumbnail((IMAGE_MAX_SIZE, IMAGE_MAX_SIZE), Image.ANTIALIAS)
    # high quality because from this image we will create thumbnails
    img.save(out_file, img.format or 'JPEG', quality=90)


def process_image(f, user_id):
    buf = BufferIO()
    if IMAGE_MAX_SIZE:
        resize_image(f, buf)
    path = default_storage.save(get_path(user_id, f.name), buf)
    return path
