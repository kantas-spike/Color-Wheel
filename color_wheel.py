"""
    Title: Colorwheel Demonstration
    Description: This demonstrates the ability of creating a color wheel color select in Tkinter
    Author: Israel Dryer
    Modified: 2020-05-30

"""
import tkinter as tk
import colorsys
import copy
import math
import glob
import re


class ColorCursor:
    COLOR_SINGLE = "Single"
    COLOR_COMPLEMENTARY = "Complementary"
    COLOR_TRIAD = "Triadic"
    COLOR_ANALOGOUS = "Analogous"
    COLOR_SPLIT_COMPLEMENTARY = "Split-complementary"
    COLOR_TETRADIC_RECT = "Rectangle"
    COLOR_TETRADIC_SQUARE = "Square"
    COLOR_TYPES = [
        COLOR_SINGLE,
        COLOR_COMPLEMENTARY,
        COLOR_SPLIT_COMPLEMENTARY,
        COLOR_TRIAD,
        COLOR_ANALOGOUS,
        COLOR_TETRADIC_RECT,
        COLOR_TETRADIC_SQUARE,
    ]

    CURSOR_META = {
        COLOR_SINGLE: {"cursor_count": 1, "others_degree": []},
        COLOR_COMPLEMENTARY: {"cursor_count": 2, "others_degree": [180]},
        COLOR_TRIAD: {"cursor_count": 3, "others_degree": [120, 240]},
        COLOR_ANALOGOUS: {"cursor_count": 3, "others_degree": [-30, 30]},
        COLOR_SPLIT_COMPLEMENTARY: {"cursor_count": 3, "others_degree": [150, 210]},
        COLOR_TETRADIC_RECT: {"cursor_count": 4, "others_degree": [60, 180, 240]},
        COLOR_TETRADIC_SQUARE: {"cursor_count": 4, "others_degree": [90, 180, 270]},
    }

    def __init__(self, x, y, center_x, center_y, color_type=COLOR_SINGLE) -> None:
        self.cur_x = x
        self.cur_y = y
        self.center_x = center_x
        self.center_y = center_y
        self.other_positions = []
        self.color_type = color_type

    def rotate(self, x, y, deg):
        rad = math.radians(deg)
        rx, ry = (x - self.center_x), (y - self.center_y)
        nx = rx * math.cos(rad) - ry * math.sin(rad) + self.center_x
        ny = rx * math.sin(rad) + ry * math.cos(rad) + self.center_y
        return int(nx), int(ny)

    def calc_all_positions(self, x, y):
        pos_list = [(x, y)]
        pos_list.extend(self.calc_other_positions(x, y))
        return pos_list

    def calc_other_positions(self, x, y):
        meta = self.CURSOR_META[self.color_type]
        return [tuple(self.rotate(x, y, d)) for d in meta["others_degree"]]

    def update_other_positions(self, x, y):
        self.other_positions.clear()
        self.other_positions.extend(self.calc_other_positions(x, y))

    def update_all_positions(self, x, y):
        self.cur_x = x
        self.cur_y = y
        self.update_other_positions(x, y)

    def update_color_type(self, color_type):
        self.color_type = color_type
        self.update_other_positions(self.cur_x, self.cur_y)


class ColorFrame(tk.Frame):
    DEFAULT_LIGHT_FONT_COLOR = [0xFF, 0xFF, 0xFF]
    DEFAULT_DARK_FONT_COLOR = [0, 0, 0]
    stock_list = []

    def __init__(self, master=None, stock=False) -> None:
        super().__init__(master)

        self.rgb_color = [255, 255, 255]
        self.font_color = [255, 255, 255]
        self.parent = master
        self.color_label = tk.StringVar()
        self.color_label.set(f"{self.format_to_hexstr(*self.rgb_color)}\n{self.format_to_hslstr(*self.rgb_color)}")
        self.color_select = tk.Label(
            self, textvariable=self.color_label, bg="white", width=20, font=("Arial", 20, "bold")
        )
        self.color_select.pack(side=tk.LEFT, fill=tk.NONE, expand=0)
        self.copy_button = tk.Button(self, text="COPY", highlightthickness=8, command=self.on_copy_clicked)
        self.copy_button.pack(side=tk.RIGHT, fill=tk.NONE, expand=0)

        self.add_button = None
        self.del_button = None

        if not stock:
            self.add_button = tk.Button(self, text="+", highlightthickness=8, command=self.on_add_clicked)
            self.add_button.pack(side=tk.RIGHT, fill=tk.NONE, expand=0)
        else:
            self.del_button = tk.Button(self, text="-", highlightthickness=8, command=self.on_del_clicked)
            self.del_button.pack(side=tk.RIGHT, fill=tk.NONE, expand=0)

    def stock_color(self):
        frm = ColorFrame(self.parent, True)
        frm.update_color(copy.copy(self.rgb_color), copy.copy(self.font_color))
        if len(self.stock_list) > 0:
            frm.pack(side=tk.BOTTOM, before=self.stock_list[-1])
        else:
            frm.pack(side=tk.BOTTOM)
        self.stock_list.append(frm)

    def on_copy_clicked(self):
        self.parent.clipboard_clear()
        self.parent.clipboard_append(self.color_select["bg"])

    def on_add_clicked(self):
        self.stock_color()

    def on_del_clicked(self):
        self.stock_list.remove(self)
        self.destroy()

    def update_color(self, rgb_color, font_color):
        self.rgb_color = rgb_color
        self.font_color = font_color
        self.hex_color = self.format_to_hexstr(*rgb_color)
        self.color_label.set(f"{self.hex_color}\n{self.format_to_hslstr(*rgb_color)}")
        self.color_select["bg"] = self.hex_color
        self.color_select["fg"] = self.format_to_hexstr(*font_color)
        self.copy_button["highlightbackground"] = self.hex_color
        self.copy_button["highlightcolor"] = self.hex_color

        if self.add_button:
            self.add_button["highlightbackground"] = self.hex_color
            self.add_button["highlightcolor"] = self.hex_color

        if self.del_button:
            self.del_button["highlightbackground"] = self.hex_color
            self.del_button["highlightcolor"] = self.hex_color

        self["bg"] = self.hex_color

    @staticmethod
    def format_to_hexstr(r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    @staticmethod
    def format_to_rgbstr(r, g, b):
        return "rgb({},{},{})".format(r, g, b)

    @staticmethod
    def format_to_hslstr(r, g, b):
        hls = colorsys.rgb_to_hls(r / 0xFF, g / 0xFF, b / 0xFF)
        return "hsl({}, {}%, {}%)".format(round(hls[0] * 360), round(hls[2] * 100), round(hls[1] * 100))

    @classmethod
    def contrast_ratio(cls, color1, color2):
        lums = []
        lums.append(cls.relative_luminace(color1))
        lums.append(cls.relative_luminace(color2))
        wk = sorted(lums, reverse=True)
        return (wk[0] + 0.05) / (wk[1] + 0.05)

    @classmethod
    def get_font_color(cls, rgb_color):
        font_color = cls.DEFAULT_LIGHT_FONT_COLOR
        ratio = cls.contrast_ratio(rgb_color, font_color)
        # print("font white: ", ratio)

        if ratio < 4.5:
            font_color = cls.DEFAULT_DARK_FONT_COLOR
            # ratio = self.contrast_ratio(rgb_color, font_color)
            # print("font black: ", ratio)

        return font_color

    @classmethod
    def srgb2rgb(cls, v):
        if v <= 0.03928:
            return v / 12.92
        else:
            return ((v + 0.055) / 1.055) ** 2.4

    @classmethod
    def relative_luminace(cls, rgb):
        r, g, b = [cls.srgb2rgb(x / 255.0) for x in rgb]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b


class ColorWheel:
    DEFAULT_BRIGHTNESS = 0.5

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Colorwheel")
        self.brightness = self.val2key(self.DEFAULT_BRIGHTNESS)

        self.setup_wheels()
        self.setup_widgets()
        self.setup_cursor()

    def start(self):
        self.update()
        self.root.mainloop()

    def update(self):
        self.redraw()
        self.update_color()

    def setup_cursor(self):
        self.canvas.update()
        self.canvas_center = (round(self.canvas.winfo_width() / 2), round(self.canvas.winfo_height() / 2))
        wheel_center = (self.wheel_radius, self.wheel_radius)
        self.wheel_offset = (wheel_center[0] - self.canvas_center[0], wheel_center[1] - self.canvas_center[1])
        self.color_cursor = ColorCursor(*self.canvas_center, *self.canvas_center)

    def setup_wheels(self):
        self.wheels = {}
        for path in sorted(glob.glob("./imgs/wheel_*.png")):
            if m := re.match(r".*/wheel_(\d+\.?\d*).png", path):
                v = float(m.group(1))
                self.wheels[self.val2key(v)] = tk.PhotoImage(file=path)

        self.wheel_width = self.wheels[self.brightness].width()
        self.wheel_height = self.wheels[self.brightness].height()
        self.wheel_radius = round(self.wheel_width / 2)

    def setup_canvas(self, frame_canvas):
        self.cursor_image = tk.PhotoImage(file="cursor.png")
        self.sub_cursor_image = tk.PhotoImage(file="sub_cursor.png")

        self.canvas = tk.Canvas(frame_canvas, height=730, width=730)
        self.canvas.pack(anchor=tk.CENTER, expand=0, pady=4, padx=4)
        self.canvas.bind("<B1-Motion>", self.on_mouse_draged)
        self.canvas.bind("<Double-Button-1>", self.on_mouse_dbclicked)

    def setup_colorframelist(self, frame_right):
        self.color_frame = ColorFrame(frame_right)
        frame_right["bg"] = "#cdcdcd"
        self.color_frame.pack(side=tk.TOP)
        self.color_frame_list = []

    def setup_brightness(self, frame_bottom):
        self.brightness_frame = tk.LabelFrame(frame_bottom, text="Lightness:")
        self.brightness_var = tk.DoubleVar()
        self.brightness_var.set(self.DEFAULT_BRIGHTNESS * 100)
        tk.Scale(
            self.brightness_frame,
            variable=self.brightness_var,
            command=self.on_brightness_changed,
            length=720,
            width=10,
            from_=0,
            to=100,
            resolution=1,
            tickinterval=5,
            orient=tk.HORIZONTAL,
        ).pack(fill=tk.X)
        self.brightness_frame.pack(fill=tk.X, side=tk.LEFT, expand=1)

    def setup_color_scheme(self, group_frame):
        self.option_value = tk.StringVar()
        self.option_value.set(ColorCursor.COLOR_SINGLE)
        for ct in ColorCursor.COLOR_TYPES:
            tk.Radiobutton(
                group_frame, text=ct, value=ct, variable=self.option_value, command=self.on_radio_changed
            ).pack(side=tk.LEFT)

    def setup_goto_color(self, input_frame):
        self.input_frame.grid(row=2, column=1, sticky=tk.EW)
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(self.input_frame, textvariable=self.input_var)
        self.input_entry.pack(side=tk.LEFT, expand=1, fill=tk.X)
        self.input_entry["bg"] = "white"
        self.input_entry["fg"] = "black"
        self.input_entry["insertbackground"] = "black"
        self.input_button = tk.Button(self.input_frame, text="GoTo", command=self.on_goto_clicked)
        self.input_button.pack(side=tk.RIGHT, ipady=1, pady=1)

    def setup_widgets(self):
        self.frame_canvas = tk.Frame(self.root)
        self.setup_canvas(self.frame_canvas)

        self.frame_right = tk.Frame(self.root)
        self.setup_colorframelist(self.frame_right)

        self.frame_bottom = tk.Frame(self.root)
        self.setup_brightness(self.frame_bottom)

        self.group_frame = tk.LabelFrame(self.root, text="Color Scheme")
        self.setup_color_scheme(self.group_frame)

        self.input_frame = tk.LabelFrame(self.root, text="Color(例: #FFFFFF):")
        self.setup_goto_color(self.input_frame)

        self.status_info = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_info, width=20, anchor=tk.W, padx=4)

        self.group_frame.grid(row=0, column=0, pady=10)
        self.frame_canvas.grid(row=1, column=0)
        self.frame_right.grid(row=0, column=1, rowspan=2, sticky=tk.N + tk.S)
        self.frame_bottom.grid(row=2, column=0, sticky=tk.W + tk.E)
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E)

    def show_status(self, msg):
        self.status_info.set(msg)

    def redraw(self):
        # clear the canvas and redraw
        self.canvas.delete("all")
        wheel = self.wheels[self.brightness]
        self.canvas.create_image(self.canvas_center[0], self.canvas_center[1], image=wheel)
        for pos in self.color_cursor.other_positions:
            self.canvas.create_image(pos[0], pos[1], image=self.sub_cursor_image)
        self.canvas.create_image(self.color_cursor.cur_x, self.color_cursor.cur_y, image=self.cursor_image)

    def get_wheel_color(self, x, y):
        wheel = self.wheels[self.brightness]
        return wheel.get(x + self.wheel_offset[0], y + self.wheel_offset[1])

    def update_color(self):
        rgb_color = self.get_wheel_color(self.color_cursor.cur_x, self.color_cursor.cur_y)

        font_color = ColorFrame.get_font_color(rgb_color)
        self.color_frame.update_color(rgb_color, font_color)

        for idx, pos in enumerate(self.color_cursor.other_positions):
            rgb_color = self.get_wheel_color(*pos)
            font_color = ColorFrame.get_font_color(rgb_color)
            self.color_frame_list[idx].update_color(rgb_color, font_color)

    def in_wheel(self, x, y):
        x += self.wheel_offset[0]
        y += self.wheel_offset[1]
        if not (0 <= x <= self.wheel_width):
            return False
        if not (0 <= y <= self.wheel_height):
            return False
        return True

    def has_color(self, x, y):
        self.canvas_center
        pos_list = self.color_cursor.calc_all_positions(x, y)
        for nx, ny in pos_list:
            if not self.in_wheel(nx, ny):
                return False
            try:
                rgb_color = self.get_wheel_color(nx, ny)
                hex_color = ColorFrame.format_to_hexstr(*rgb_color)
                if hex_color == "#000000":
                    return False
            except tk.TclError as err:
                print("has_color: ignore TclError", err)
                return False

        return True

    def on_mouse_draged(self, event):
        """Mouse movement callback"""
        if not self.has_color(event.x, event.y):
            return

        # get mouse coordinates
        self.color_cursor.update_all_positions(event.x, event.y)

        self.redraw()
        self.update_color()

    def on_radio_changed(self):
        color_type = self.option_value.get()
        self.color_cursor.update_color_type(color_type)

        for cf in self.color_frame_list:
            cf.destroy()
        self.color_frame_list.clear()

        for _ in self.color_cursor.other_positions:
            cf = ColorFrame(self.frame_right)
            cf.pack(side=tk.TOP, after=self.color_frame)
            self.color_frame_list.append(cf)

        self.redraw()
        self.update_color()

    def on_mouse_dbclicked(self, event):
        """Mouse movement callback"""
        if not self.has_color(event.x, event.y):
            return

        self.color_cursor.update_all_positions(event.x, event.y)

        self.redraw()
        self.update_color()

    def on_brightness_changed(self, event=None):
        val = self.brightness_var.get()
        self.brightness = self.val2key(float(val) / 100)
        self.redraw()
        self.update_color()

    def on_goto_clicked(self):
        val = self.input_var.get()
        if result := re.match(r"#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})", val):
            r = int(result.group(1), 16)
            g = int(result.group(2), 16)
            b = int(result.group(3), 16)
            hls = colorsys.rgb_to_hls(r / 0xFF, g / 0xFF, b / 0xFF)
            x, y = self.get_color_pos(hls)
            self.input_var.set("")
            self.input_entry["bg"] = "white"
            normalized_brightness = round(hls[1], 2)
            self.brightness_var.set(normalized_brightness * 100)
            self.brightness = self.val2key(normalized_brightness)

            self.color_cursor.update_all_positions(x, y)
            self.redraw()
            self.update_color()
            if self.color_frame.hex_color != val:
                self.show_status(
                    "goto to {} instead of {}: there is no wheel that matches the lightness of {}(L: {})".format(
                        self.color_frame.hex_color, val, val, hls[1]
                    )
                )
            else:
                self.show_status(f"goto: {val}")
        else:
            self.input_entry["bg"] = "#ffcccc"
            self.show_status(f"invalid color: {val}")

    def val2key(self, val):
        return "{:0.2f}".format(val)

    def get_color_pos(self, hls):
        rad = (hls[0] * math.pi * 2) - math.pi / 2
        rx = int(math.cos(rad) * self.wheel_radius * hls[2])
        ry = int(math.sin(rad) * self.wheel_radius * hls[2])
        x = rx + self.wheel_radius - self.wheel_offset[0]
        y = ry + self.wheel_radius - self.wheel_offset[1]
        return (x, y)


if __name__ == "__main__":
    w = ColorWheel()
    w.start()
