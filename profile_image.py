"""Create an original, minimal avatar for IA DEL REY at runtime."""
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


def _font(size: int):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        try:
            return ImageFont.load_default(size=size)
        except TypeError:
            return ImageFont.load_default()


def make_profile_photo() -> bytes:
    """Return a 512x512 JPEG suitable for Telegram setMyProfilePhoto."""
    img = Image.new("RGB", (512, 512), "#101C35")
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((32, 32, 480, 480), radius=92,
                           fill="#1A3051", outline="#D9B76D", width=10)
    draw.ellipse((116, 90, 396, 370),
                 fill="#233D60", outline="#E9C77D", width=7)
    # Crown artwork is drawn with shapes, without external images or fonts.
    draw.polygon([(173, 189), (171, 140), (218, 167),
                  (256, 122), (294, 167), (341, 140), (339, 189)],
                 fill="#F0CA75")
    draw.rounded_rectangle((172, 185, 340, 204), radius=6, fill="#F0CA75")
    draw.text((256, 275), "IA", anchor="mm",
              font=_font(112), fill="#FFFFFF")
    draw.text((256, 417), "DEL REY", anchor="mm",
              font=_font(42), fill="#F0CA75")
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=92, optimize=True)
    return buffer.getvalue()
