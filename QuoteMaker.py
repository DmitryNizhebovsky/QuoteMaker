from PIL import Image, ImageDraw, ImageFont

class QuoteMaker:
    def __init__(self, msg_font_color = None, msg_background_color = None, nickname_font_color = None):
        self.msg_font_color = msg_font_color or (255, 255, 255, 255)
        self.msg_background_color = msg_background_color or (30, 50, 80, 255)
        self.nickname_font_color = nickname_font_color or (160, 39, 160, 255)
        self.avatar_size = 50
        self.sticker_max_size = 512
        self.msg_font_size = 16
        self.nickname_font_size = 16
        self.nickname_font_name = './fonts/SF-UI-Text-Bold.ttf'
        self.nickname_font = ImageFont.truetype(self.nickname_font_name, self.nickname_font_size)
        self.msg_font_name = './fonts/SF-UI-Text-Regular.ttf'
        self.msg_font = ImageFont.truetype(self.msg_font_name, self.msg_font_size)
        self.avatar_margin_top = 0
        self.avatar_margin_left = 0
        self.msg_bubble_corner_radius = 10
        self.msg_bubble_margin_top = 0
        self.msg_bubble_margin_left = 10
        self.nickname_margin_left = 8
        self.nickname_margin_top = 5
        self.msg_margin_left = 8
        self.msg_margin_right = 8
        self.msg_margin_top = 5
        self.msg_margin_bottom = 10

    def create_quote(self, avatar_img, message, nickname):
        canvas = Image.new('RGBA', (self.sticker_max_size, self.sticker_max_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        msg_bubble_max_width = self.sticker_max_size - self.avatar_size - self.msg_bubble_margin_left
        max_line_width = msg_bubble_max_width - self.msg_margin_left - self.msg_margin_right
        splitted_message = self.__split_message(message, max_line_width, draw)

        avatar = self.__draw_avatar(avatar_img)
        avatar_pos = (self.avatar_margin_left , self.avatar_margin_top)
        canvas.paste(avatar, avatar_pos)

        msg_bubble_rect = self.__calculate_msg_bubble_rect(splitted_message, nickname, msg_bubble_max_width, draw)
        msg_bubble = self.__round_rectangle(msg_bubble_rect, self.msg_bubble_corner_radius, self.msg_background_color)

        msg_bubble_pos = (self.avatar_size + self.msg_bubble_margin_left, self.msg_bubble_margin_top)
        canvas.paste(msg_bubble, msg_bubble_pos)

        nickname_pos = (msg_bubble_pos[0] + self.nickname_margin_left, self.nickname_margin_top)
        draw.text(nickname_pos, nickname, font=self.nickname_font, fill=self.nickname_font_color)

        _, nickname_height = draw.textsize(nickname, font=self.nickname_font)
        current_height = msg_bubble_pos[1] + nickname_height + self.nickname_margin_top + self.msg_margin_top

        for line in splitted_message:
            _, line_height = draw.textsize(line, font=self.msg_font)
            draw.text((msg_bubble_pos[0] + self.msg_margin_left, current_height), line, font=self.msg_font)
            current_height += line_height

        crop_width, crop_height = self.sticker_max_size, self.sticker_max_size
        msg_bubble_horizontal_end = msg_bubble_pos[0] + msg_bubble_rect[0]
        msg_bubble_vertical_end = msg_bubble_pos[1] + msg_bubble_rect[1]

        if msg_bubble_horizontal_end < self.sticker_max_size:
            crop_width = msg_bubble_horizontal_end
        if msg_bubble_vertical_end < self.sticker_max_size:
            if msg_bubble_vertical_end <= self.avatar_size + self.avatar_margin_top:
                crop_height = self.avatar_size + self.avatar_margin_top
            else:
                crop_height = msg_bubble_vertical_end

        crop_canvas = canvas.crop((0, 0, crop_width, crop_height))
        return crop_canvas

    def __round_corner(self, radius, fill):
        """Draw a round corner"""
        antialias = 4
        corner = Image.new('RGBA', (antialias * radius, antialias * radius), (0, 0, 0, 0))
        draw = ImageDraw.Draw(corner)
        draw.pieslice((0, 0, radius * 2 * antialias, radius * 2 * antialias), 180, 270, fill=fill)
        return corner.resize((radius, radius), Image.LANCZOS)


    def __round_rectangle(self, size, radius, fill):
        """Draw a rounded rectangle"""
        width, height = size
        rectangle = Image.new('RGBA', size, fill)
        corner = self.__round_corner(radius, fill)
        rectangle.paste(corner, (0, 0))
        rectangle.paste(corner.rotate(90), (0, height - radius))
        rectangle.paste(corner.rotate(180), (width - radius, height - radius))
        rectangle.paste(corner.rotate(270), (width - radius, 0))
        return rectangle

    def __draw_avatar(self, avatar_img):
        avatar_img = avatar_img.resize((self.avatar_size, self.avatar_size))
        big_size = (avatar_img.size[0] * 3, avatar_img.size[1] * 3)
        mask = Image.new('L', big_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + big_size, fill=255)
        mask = mask.resize(avatar_img.size, Image.ANTIALIAS)
        avatar_img.putalpha(mask)
        return avatar_img

    def __calculate_msg_bubble_rect(self, splitted_message, nickname, msg_bubble_max_width, draw):
        msg_height = 0

        for line in splitted_message:
            _, line_height = draw.textsize(line, font=self.msg_font)
            msg_height += line_height

        nickname_width, nickname_height = draw.textsize(nickname, font=self.nickname_font)
        msg_bubble_height = msg_height + self.msg_margin_bottom + self.msg_margin_top \
            + self.nickname_margin_top + nickname_height

        msg_bubble_width = 0
        if len(splitted_message) > 1:
            msg_bubble_width = msg_bubble_max_width 
        else:
            line_width, _ = draw.textsize(splitted_message[0], font=self.msg_font)
            if line_width < nickname_width:
                msg_bubble_width = nickname_width + self.msg_margin_right + self.msg_margin_left
            else:
                msg_bubble_width = line_width + self.msg_margin_right + self.msg_margin_left

        return (msg_bubble_width, msg_bubble_height)

    def __split_message(self, message, max_line_width, draw):
        words = message.split(' ')
        words = list(filter(None, words))

        msg_lines = []
        msg_line= ''
        temp_msg_line = ''

        for word in words:
            temp_msg_line = msg_line + word + ' '
            line_width, _ = draw.textsize(temp_msg_line, font=self.msg_font)

            if (line_width <= max_line_width):
                msg_line = temp_msg_line
            elif (line_width > max_line_width):
                msg_lines.append(msg_line.strip())
                msg_line = word + ' '

        if len(msg_line) > 0:
            msg_lines.append(msg_line.strip())

        return msg_lines