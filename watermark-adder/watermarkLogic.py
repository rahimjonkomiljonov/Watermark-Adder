from PIL import Image, ImageDraw, ImageFont


class WatermarkLogic:
    def convert_color_to_hex(self, color, opacity_percent):
        opacity_hex = hex(int(opacity_percent * 255 / 100))[2:].upper().zfill(2)
        if color.startswith("#"):
            if len(color) == 7:
                return color + opacity_hex
            return color
        named_colors = {
            "white": "#FFFFFF",
            "black": "#000000",
            "red": "#FF0000",
            "green": "#00FF00",
            "blue": "#0000FF",
        }
        hex_color = named_colors.get(color.lower(), "#FFFFFF")
        return hex_color + opacity_hex

    def add_watermark(self, image, text, position, font_size, color, font_name, opacity, watermark_image=None):
        watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)

        img_width, img_height = image.size
        margin = 15

        if watermark_image:
            wm_width, wm_height = watermark_image.size
            scale = min((img_width * 0.3) / wm_width, (img_height * 0.3) / wm_height)
            new_size = (int(wm_width * scale), int(wm_height * scale))
            watermark_image = watermark_image.resize(new_size, Image.Resampling.LANCZOS)

            wm_width, wm_height = watermark_image.size
            if position == "Top Left":
                x, y = margin, margin
            elif position == "Top Center":
                x, y = (img_width - wm_width) // 2, margin
            elif position == "Top Right":
                x, y = img_width - wm_width - margin, margin
            elif position == "Center Left":
                x, y = margin, (img_height - wm_height) // 2
            elif position == "Center":
                x, y = (img_width - wm_width) // 2, (img_height - wm_height) // 2
            elif position == "Center Right":
                x, y = img_width - wm_width - margin, (img_height - wm_height) // 2
            elif position == "Bottom Left":
                x, y = margin, img_height - wm_height - margin
            elif position == "Bottom Center":
                x, y = (img_width - wm_width) // 2, img_height - wm_height - margin
            else:
                x, y = img_width - wm_width - margin, img_height - wm_height - margin

            watermark_layer.paste(watermark_image, (x, y), watermark_image)
        else:
            font_files = {
                "Arial": "arial.ttf",
                "Times New Roman": "times.ttf",
                "Courier New": "cour.ttf",
            }
            selected_font_file = font_files.get(font_name, "arial.ttf")
            try:
                font = ImageFont.truetype(selected_font_file, font_size)
            except Exception:
                font = ImageFont.load_default()

            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            if position == "Top Left":
                x, y = margin, margin
            elif position == "Top Center":
                x, y = (img_width - text_width) // 2, margin
            elif position == "Top Right":
                x, y = img_width - text_width - margin, margin
            elif position == "Center Left":
                x, y = margin, (img_height - text_height) // 2
            elif position == "Center":
                x, y = (img_width - text_width) // 2, (img_height - text_height) // 2
            elif position == "Center Right":
                x, y = img_width - text_width - margin, (img_height - text_height) // 2
            elif position == "Bottom Left":
                x, y = margin, img_height - text_height - margin
            elif position == "Bottom Center":
                x, y = (img_width - text_width) // 2, img_height - text_height - margin
            else:
                x, y = img_width - text_width - margin, img_height - text_height - margin

            color_with_opacity = self.convert_color_to_hex(color, opacity)
            shadow_color = "#00000080"
            draw.text((x + 2, y + 2), text, font=font, fill=shadow_color)
            draw.text((x, y), text, font=font, fill=color_with_opacity)

        return Image.alpha_composite(image, watermark_layer)

    