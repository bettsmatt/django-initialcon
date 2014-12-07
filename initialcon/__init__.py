import hashlib
import StringIO
from os.path import abspath, dirname, join

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

from django.shortcuts import render
from django.http import HttpResponse
from django.conf.urls import patterns, url
from django.conf import settings

# A font is required
fonts = getattr(settings, 'INITIALCON_FONTS', None)


# Default settings
DEFAULT_SETTINGS = {
    'INITIALCON_SIZE': 100,
    'INITIALCON_SIZE_MAX': 200,
    'INITIALCON_COLORS': [
        (153,180,51), (0,163,0), (30,113,69), (255,0,151), (45,137,239),
        (159,0,167), (0,171,169), (185,29,71),(227,162,26), (255,196,13),
        (126,56,120), (96,60,186), (43,87,151), (218,83,44), (238,17,17)],
    'INITIALCON_FONTS': None
}

# Try override
fonts = getattr(settings, 'INITIALCON_FONTS', DEFAULT_SETTINGS['INITIALCON_FONTS'])
colors = getattr(settings, 'INITIALCON_COLORS', DEFAULT_SETTINGS['INITIALCON_COLORS'])
size_default = getattr(settings, 'INITIALCON_SIZE', DEFAULT_SETTINGS['INITIALCON_SIZE'])
size_max = getattr(settings, 'INITIALCON_SIZE_MAX', DEFAULT_SETTINGS['INITIALCON_SIZE_MAX'])

# Missing fonts
if fonts is None:
    raise LookupError(
        """
INITIALCON_FONTS must be configured in your settings.py
INITIALCON_FONTS = {
    'default': '<pathtofont>',
    'special': '<pathtofont>'
}
        """)

# Single url for generating initialcons
urlpatterns = patterns('initialcon',
    url(r'^(?P<name>.+)$', 'generate', name='generate'),
)

# Returns the initials of the name
def get_initials(name, sep=''):
    return sep.join([word[0] for word in name.split(' ')[:2]])

def generate(request, name):
    """
    Generate initialcons for a given name as a .png.
    Accepts custom size and font as query parameters.
    """

    name = name.encode('utf-8').upper()

    # Custom size
    size = request.GET.get('size', False)
    if size and size.isdigit():
        size = int(size)
    else:
        size = size_default

    # Stop from being crazy big
    size = min(size, size_max)

    # Custom font
    font = request.GET.get('font', False)
    if font and font in fonts:
        font = fonts[font]
    else:
        font = fonts.values()[0]

    # Consistent color based on name
    encoded = hashlib.md5(name)
    color_index = int(encoded.hexdigest(), 16)
    color = colors[color_index % len(colors)]

    # Take the first two initals
    initials = get_initials(name)
    font = ImageFont.truetype(font, int(size*0.5))
    img = Image.new("RGBA", (size, size),color)
    draw = ImageDraw.Draw(img)

    w, h = font.getsize(initials)

    # Account for vertical offset to center
    h = h + font.getoffset(initials)[1]

    x = (size - w) / 2
    y = (size - h) / 2

    # Draw
    draw.text((x, y), initials,font=font)
    draw = ImageDraw.Draw(img)

    # Output as PNG
    output = StringIO.StringIO()
    img.save(output, format="PNG")

    return HttpResponse(output.getvalue(), content_type="image/png")
