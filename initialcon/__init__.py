import hashlib
import StringIO
from datetime import timedelta, datetime

from PIL import ImageFont, Image, ImageDraw

from django.http import HttpResponse
from django.conf.urls import patterns, url
from django.conf import settings
from django.utils import cache

# A font is required
fonts = getattr(settings, 'INITIALCON_FONTS', None)

# Default settings
DEFAULT_SETTINGS = {
    'INITIALCON_SIZE': 100,
    'INITIALCON_SIZE_MAX': 200,
    'INITIALCON_COLORS': [
        (153, 180, 51), (0, 163, 0), (30, 113, 69), (255, 0, 151), (45, 137, 239),
        (159, 0, 167), (0, 171, 169), (185, 29, 71), (227, 162, 26), (255, 196, 13),
        (126, 56, 120), (96, 60, 186), (43, 87, 151), (218, 83, 44), (238, 17, 17)],
    'INITIALCON_FONTS': None,
    'INITIALCON_FONT_COLOR': (255, 255, 255),
    'INITIALCON_FONT_SIZE': 0.5,
    'INITIALCON_FONTS': None,
    'INITIALCON_EXPIRES_TIME': timedelta(days=14)
}

# Try override
fonts = getattr(settings, 'INITIALCON_FONTS', DEFAULT_SETTINGS['INITIALCON_FONTS'])
colors = getattr(settings, 'INITIALCON_COLORS', DEFAULT_SETTINGS['INITIALCON_COLORS'])
font_color = getattr(settings, 'INITIALCON_FONT_COLOR', DEFAULT_SETTINGS['INITIALCON_FONT_COLOR'])
font_size = getattr(settings, 'INITIALCON_FONT_SIZE', DEFAULT_SETTINGS['INITIALCON_FONT_SIZE'])
size_default = getattr(settings, 'INITIALCON_SIZE', DEFAULT_SETTINGS['INITIALCON_SIZE'])
size_max = getattr(settings, 'INITIALCON_SIZE_MAX', DEFAULT_SETTINGS['INITIALCON_SIZE_MAX'])
expires_time = getattr(settings, 'INITIALCON_EXPIRES_TIME', DEFAULT_SETTINGS['INITIALCON_EXPIRES_TIME'])

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
urlpatterns = patterns(
    'initialcon',
    url(r'^(?P<name>.+)$', 'generate', name='generate'),
)


# Returns the initials of the name
def get_initials(name, sep=''):
    if name:

        # grabs the first letter of each token in the name
        initials = [word[0] for word in name.split()]

        if len(initials) == 1:

            # only one initial
            return initials[0]

        # join the first and last of multiple initials
        return sep.join([initials[0], initials[-1]])

    return ''


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
    font = ImageFont.truetype(font, int(size * font_size))
    img = Image.new("RGBA", (size, size), color)
    draw = ImageDraw.Draw(img)

    w, h = font.getsize(initials)

    # Account for vertical offset to center
    h = h + font.getoffset(initials)[1]

    x = (size - w) / 2
    y = (size - h) / 2

    # Draw
    draw.text((x, y), initials, font=font, fill=font_color)
    draw = ImageDraw.Draw(img)

    # Output as PNG
    output = StringIO.StringIO()
    img.save(output, format="PNG")

    response = HttpResponse(output.getvalue(), content_type="image/png")

    # Attempt to cache, fix later
    now = datetime.now()
    expires_at = now + expires_time
    total_seconds = int((expires_at - now).total_seconds())
    cache.patch_response_headers(response, total_seconds)
    return response
