"""
    Title: Colorwheel Demonstration
    Description: This demonstrates the ability of creating a color wheel color select in Tkinter
    Author: Israel Dryer
    Modified: 2020-05-30

"""
import tkinter as tk
import copy
import math


class ColorCursor:
    COLOR_SINGLE = "Single"
    COLOR_COMPLEMENTARY = "Complementary"
    COLOR_TRIAD = "Triadic"
    COLOR_ANALOGOUS = "Analogous"
    COLOR_SPLIT_COMPLEMENTARY = "Split-complementary"
    COLOR_TYPES = [COLOR_SINGLE, COLOR_COMPLEMENTARY, COLOR_SPLIT_COMPLEMENTARY, COLOR_TRIAD, COLOR_ANALOGOUS]

    CURSOR_META = {
        COLOR_SINGLE: {"cursor_count": 1, "others_degree": []},
        COLOR_COMPLEMENTARY: {"cursor_count": 2, "others_degree": [180]},
        COLOR_TRIAD: {"cursor_count": 3, "others_degree": [120, 240]},
        COLOR_ANALOGOUS: {"cursor_count": 3, "others_degree": [-30, 30]},
        COLOR_SPLIT_COMPLEMENTARY: {"cursor_count": 3, "others_degree": [150, 210]},
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

    def setup_positions(self, x, y):
        self.other_positions.clear()
        meta = self.CURSOR_META[self.color_type]
        for d in meta["others_degree"]:
            self.other_positions.append(tuple(self.rotate(x, y, d)))

    def update_position(self, x, y):
        self.cur_x = x
        self.cur_y = y
        self.setup_positions(x, y)

    def update_color_type(self, color_type):
        self.color_type = color_type
        self.setup_positions(self.cur_x, self.cur_y)


class ColorFrame(tk.Frame):
    def __init__(self, master=None, stock=False) -> None:
        super().__init__(master)

        self.rgb_color = [255, 255, 255]
        self.font_color = [255, 255, 255]
        self.parent = master
        self.color_label = tk.StringVar()
        self.color_label.set("#FFFFFF\nrgb(255,255,255)")
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
        frm.pack(side=tk.BOTTOM, after=self)

    def on_copy_clicked(self):
        self.parent.clipboard_clear()
        self.parent.clipboard_append(self.color_select["bg"])

    def on_add_clicked(self):
        self.stock_color()

    def on_del_clicked(self):
        self.destroy()

    def update_color(self, rgb_color, font_color):
        self.rgb_color = rgb_color
        self.font_color = font_color
        hex_color = "#{:02x}{:02x}{:02x}".format(*rgb_color)
        self.color_label.set(hex_color + "\nrgb({},{},{})".format(*rgb_color))
        self.color_select["bg"] = hex_color
        self.color_select["fg"] = "#{:02x}{:02x}{:02x}".format(*font_color)
        self.copy_button["highlightbackground"] = hex_color
        self.copy_button["highlightcolor"] = hex_color

        if self.add_button:
            self.add_button["highlightbackground"] = hex_color
            self.add_button["highlightcolor"] = hex_color

        if self.del_button:
            self.del_button["highlightbackground"] = hex_color
            self.del_button["highlightcolor"] = hex_color

        self["bg"] = hex_color


class ColorWheel:
    def __init__(self) -> None:
        self.setup_widgets()
        self.wheel_width = self.wheels[self.scale].width()
        self.wheel_height = self.wheels[self.scale].height()
        self.target_width = self.target.width()
        self.target_height = self.target.height()

    def start(self):
        self.update()
        self.root.mainloop()

    def update(self):
        self.redraw()
        self.update_color()

    def setup_widgets(self):
        self.scale = self.val2key(1.0)

        self.root = tk.Tk()
        self.root.title("Colorwheel")
        frame_canvas = tk.Frame(self.root)
        self.frame_right = tk.Frame(self.root)
        frame_bottom = tk.Frame(self.root)
        self.group_frame = tk.LabelFrame(self.root, text="Color Scheme")

        self.option_value = tk.StringVar()
        self.option_value.set(ColorCursor.COLOR_SINGLE)
        for ct in ColorCursor.COLOR_TYPES:
            tk.Radiobutton(
                self.group_frame, text=ct, value=ct, variable=self.option_value, command=self.on_radio_changed
            ).pack(side=tk.LEFT)

        self.canvas = tk.Canvas(frame_canvas, height=730, width=730)
        self.canvas.pack(anchor=tk.CENTER, expand=0, pady=4, padx=4)
        self.canvas.bind("<B1-Motion>", self.on_mouse_draged)
        self.canvas.bind("<Double-Button-1>", self.on_mouse_dbclicked)

        v_var = tk.DoubleVar(value=1.0)
        v_scale = tk.Scale(
            frame_bottom,
            variable=v_var,
            orient=tk.HORIZONTAL,
            from_=0.1,
            to=1.0,
            resolution=0.1,
            command=self.on_scaled,
            label="Brightness:",
        )
        v_scale.pack(fill=tk.X, side=tk.LEFT, expand=1)

        self.color_frame = ColorFrame(self.frame_right)
        self.color_frame.pack(side=tk.TOP)
        self.color_frame_list = []

        self.wheels = {}
        v = 0.1
        while v <= 1.0:
            self.wheels[self.val2key(v)] = tk.PhotoImage(file="./imgs/wheel_{:0.2f}.png".format(v))
            v += 0.1

        self.target = tk.PhotoImage(file="target.png")
        self.sub_target = tk.PhotoImage(file="sub_target.png")

        self.group_frame.grid(row=0, column=0, pady=10)
        frame_canvas.grid(row=1, column=0)
        self.frame_right.grid(row=0, column=1, rowspan=3, sticky=tk.N + tk.S)
        frame_bottom.grid(row=2, column=0, sticky=tk.W + tk.E)

        self.canvas.update()
        self.canvas_center = (self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2)
        self.color_cursor = ColorCursor(*self.canvas_center, *self.canvas_center)

    def redraw(self):
        # clear the canvas and redraw
        self.canvas.delete("all")
        wheel = self.wheels[self.scale]
        self.canvas.create_image(self.canvas_center[0], self.canvas_center[1], image=wheel)
        for pos in self.color_cursor.other_positions:
            self.canvas.create_image(pos[0], pos[1], image=self.sub_target)
        self.canvas.create_image(self.color_cursor.cur_x, self.color_cursor.cur_y, image=self.target)

    def contrast_ratio(self, color1, color2):
        lums = []
        lums.append(self.relative_luminace(color1))
        lums.append(self.relative_luminace(color2))
        wk = sorted(lums, reverse=True)
        return (wk[0] + 0.05) / (wk[1] + 0.05)

    def get_font_color(self, rgb_color):
        font_color = [0xFF, 0xFF, 0xFF]  # white
        ratio = self.contrast_ratio(rgb_color, font_color)
        # print("font white: ", ratio)

        if ratio < 4.5:
            font_color = [0, 0, 0]  # black
            # ratio = self.contrast_ratio(rgb_color, font_color)
            # print("font black: ", ratio)

        return font_color

    def update_color(self):
        # get rgb color from pixel location in image
        wheel = self.wheels[self.scale]
        rgb_color = wheel.get(self.color_cursor.cur_x, self.color_cursor.cur_y)

        font_color = self.get_font_color(rgb_color)
        self.color_frame.update_color(rgb_color, font_color)
        self.frame_right["bg"] = "#{:02x}{:02x}{:02x}".format(*rgb_color)

        for idx, pos in enumerate(self.color_cursor.other_positions):
            rgb_color = wheel.get(*pos)
            font_color = self.get_font_color(rgb_color)
            self.color_frame_list[idx].update_color(rgb_color, font_color)

    def has_color(self, x, y):
        self.canvas_center
        radius = self.wheel_width // 2

        wheel = self.wheels[self.scale]

        if x < self.canvas_center[0] - radius or x > self.canvas_center[0] + radius:
            return False
        if y < self.canvas_center[1] - radius or y > self.canvas_center[1] + radius:
            return False

        rgb_color = wheel.get(x, y)
        hex_color = "#{:02x}{:02x}{:02x}".format(*rgb_color)
        if hex_color == "#000000":
            return False
        else:
            return True

    def on_mouse_draged(self, event):
        """Mouse movement callback"""
        if not self.has_color(event.x, event.y):
            return

        # get mouse coordinates
        self.color_cursor.update_position(event.x, event.y)

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

        # get mouse coordinates
        self.color_cursor.update_position(event.x, event.y)

        self.redraw()
        self.update_color()

    def on_scaled(self, val):
        self.scale = self.val2key(float(val))
        self.redraw()
        self.update_color()

    def val2key(self, val):
        return "{:0.2f}".format(val)

    def srgb2rgb(self, v):
        if v <= 0.03928:
            return v / 12.92
        else:
            return ((v + 0.055) / 1.055) ** 2.4

    def relative_luminace(self, rgb):
        r, g, b = [self.srgb2rgb(x / 255.0) for x in rgb]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b


if __name__ == "__main__":
    w = ColorWheel()
    w.start()
