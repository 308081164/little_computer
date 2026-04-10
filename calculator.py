import math
import random
import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox


BG = "#F4FDE6"
PANEL_BG = "#E8F7B6"
BTN_BG = "#D7F28A"
BTN_TEXT = "#1F4D1A"
OP_BG = "#A4D65E"
EQ_BG = "#4FAE4E"
DISPLAY_BG = "#FFF9C4"

PIXEL_SCALE = 3
CAT_COLORS = {
    "B": "#3A314B",
    "F": "#FFDFF0",
    "E": "#FF9BC4",
    "K": "#2A1F37",
    "M": "#D86F92",
}
CAT_SPRITES = {
    "idle": [
        "...BB......BB...",
        "..BFFB....BFFB..",
        "..BFFFBBBBFFFB..",
        ".BFFFFFFFFFFFFB.",
        ".BFFKFFFFFKFFFB.",
        ".BFFFFFFFFFFFFB.",
        ".BFFFBBBBBBFFFB.",
        "..BFFB....BFFB..",
        "..BFB......BFB..",
        "..BB........BB..",
    ],
    "blink": [
        "...BB......BB...",
        "..BFFB....BFFB..",
        "..BFFFBBBBFFFB..",
        ".BFFFFFFFFFFFFB.",
        ".BFFKFFFFFKFFFB.",
        ".BFFBBBBBBBBFFB.",
        ".BFFFFFFFFFFFFB.",
        "..BFFB....BFFB..",
        "..BFB......BFB..",
        "..BB........BB..",
    ],
    "walk_a": [
        "...BB......BB...",
        "..BFFB....BFFB..",
        "..BFFFBBBBFFFB..",
        ".BFFFFFFFFFFFFB.",
        ".BFFKFFFFFKFFFB.",
        ".BFFFFFFFFFFFFB.",
        ".BFFFBBBBBBFFFB.",
        "..BFFB....BFFB..",
        "..BFB....B..FB..",
        "..BB......BB....",
    ],
    "walk_b": [
        "...BB......BB...",
        "..BFFB....BFFB..",
        "..BFFFBBBBFFFB..",
        ".BFFFFFFFFFFFFB.",
        ".BFFKFFFFFKFFFB.",
        ".BFFFFFFFFFFFFB.",
        ".BFFFBBBBBBFFFB.",
        "..BFFB....BFFB..",
        "..BF..BFB....B..",
        "....BB......BB..",
    ],
    "sleep": [
        "................",
        "...BBBBBBBBBB...",
        "..BFFFFFFFFFFB..",
        ".BFFFFFFFFFFFFB.",
        ".BFFBBBBBBBBFFB.",
        ".BFFFFFFFFFFFFB.",
        ".BFFBEEFFEEBFFB.",
        "..BFFBBBBBBFFB..",
        "...BB......BB...",
        "................",
    ],
}


class CalculatorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Little Computer")
        self.root.geometry("420x620")
        self.root.minsize(380, 560)
        self.root.configure(bg=BG)

        self.expression = ""
        self.display_value = tk.StringVar(value="0")
        self.display_fonts = [
            tkfont.Font(family="Segoe UI", size=30, weight="bold"),
            tkfont.Font(family="Segoe UI", size=24, weight="bold"),
            tkfont.Font(family="Segoe UI", size=20, weight="bold"),
        ]
        self.display_canvas: tk.Canvas | None = None
        self.display_text_id: int | None = None
        self.cat_x = 14.0
        self.cat_y = 72.0
        self.cat_target_x = 14.0
        self.cat_min_x = 12.0
        self.cat_max_x = 250.0
        self.cat_state = "idle"
        self.cat_tick = 0
        self.cat_push_ticks = 0
        self.cat_sleep_ticks = 0

        self._build_ui()
        self._set_display("0", source="init")
        self._animate_cat()

    def _build_ui(self) -> None:
        frame = tk.Frame(self.root, bg=PANEL_BG, bd=0, highlightthickness=0)
        frame.pack(fill="both", expand=True, padx=14, pady=14)

        self.display_canvas = tk.Canvas(
            frame,
            bg=DISPLAY_BG,
            bd=0,
            highlightthickness=0,
            relief="flat",
            height=122,
        )
        self.display_canvas.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=6, pady=(8, 16))
        self.display_canvas.bind("<Configure>", self._on_display_resize)
        self.display_text_id = self.display_canvas.create_text(
            390,
            34,
            text="0",
            anchor="e",
            font=self.display_fonts[0],
            fill=BTN_TEXT,
            tags=("display-text",),
        )
        self.display_canvas.create_line(12, 96, 390, 96, fill="#E6DDA2", width=2, tags=("display-track",))

        buttons = [
            ("%", self._append),
            ("CE", self._clear_entry),
            ("C", self._clear_all),
            ("\u232b", self._backspace),
            ("1/x", self._reciprocal),
            ("x²", self._square),
            ("√x", self._sqrt),
            ("÷", self._append),
            ("7", self._append),
            ("8", self._append),
            ("9", self._append),
            ("×", self._append),
            ("4", self._append),
            ("5", self._append),
            ("6", self._append),
            ("-", self._append),
            ("1", self._append),
            ("2", self._append),
            ("3", self._append),
            ("+", self._append),
            ("+/-", self._toggle_sign),
            ("0", self._append),
            (".", self._append),
            ("=", self._calculate),
        ]

        for i, (label, handler) in enumerate(buttons):
            r = i // 4 + 1
            c = i % 4
            color = EQ_BG if label == "=" else OP_BG if label in {"+", "-", "×", "÷"} else BTN_BG
            btn = tk.Button(
                frame,
                text=label,
                font=("Segoe UI", 18, "bold"),
                bg=color,
                fg=BTN_TEXT,
                activebackground="#EAF8C6",
                activeforeground=BTN_TEXT,
                relief="flat",
                bd=0,
                command=lambda t=label, h=handler: h(t),
            )
            btn.grid(row=r, column=c, sticky="nsew", padx=5, pady=5, ipady=14)

        for r in range(7):
            frame.grid_rowconfigure(r, weight=1)
        for c in range(4):
            frame.grid_columnconfigure(c, weight=1)

    def _append(self, token: str) -> None:
        if self.display_value.get() == "0" and token not in {".", "+", "-", "×", "÷"}:
            self.expression = token
        else:
            self.expression += token
        self._set_display(self.expression or "0", source="input")

    def _clear_entry(self, _: str) -> None:
        self.expression = ""
        self._set_display("0", source="clear")

    def _clear_all(self, _: str) -> None:
        self.expression = ""
        self._set_display("0", source="clear")

    def _backspace(self, _: str) -> None:
        self.expression = self.expression[:-1]
        self._set_display(self.expression or "0", source="input")

    def _toggle_sign(self, _: str) -> None:
        if not self.expression:
            self.expression = "-"
        else:
            try:
                value = float(self.expression)
                self.expression = self._format_number(-value)
            except ValueError:
                self.expression = f"-({self.expression})"
        self._set_display(self.expression or "0", source="input")

    def _square(self, _: str) -> None:
        self._unary_operation(lambda x: x * x)

    def _sqrt(self, _: str) -> None:
        def sqrt_fn(value: float) -> float:
            if value < 0:
                raise ValueError("不能对负数开方")
            return math.sqrt(value)

        self._unary_operation(sqrt_fn)

    def _reciprocal(self, _: str) -> None:
        def rec_fn(value: float) -> float:
            if value == 0:
                raise ZeroDivisionError("0 没有倒数")
            return 1 / value

        self._unary_operation(rec_fn)

    def _unary_operation(self, fn) -> None:
        text = self.display_value.get()
        try:
            value = float(text)
            result = fn(value)
            self.expression = self._format_number(result)
            self._set_display(self.expression, source="result")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("计算错误", str(exc))

    def _calculate(self, _: str) -> None:
        try:
            sanitized = self.expression.replace("×", "*").replace("÷", "/")
            result = eval(sanitized, {"__builtins__": {}}, {})
            self.expression = self._format_number(result)
            self._set_display(self.expression, source="result")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("计算错误", f"表达式无效: {exc}")

    def _set_display(self, text: str, source: str) -> None:
        shown = text or "0"
        self.display_value.set(shown)
        self._render_display_text(shown)
        self._react_to_display(shown, source)

    def _render_display_text(self, text: str) -> None:
        if not self.display_canvas or self.display_text_id is None:
            return
        width = max(self.display_canvas.winfo_width(), 340) - 24
        selected = self.display_fonts[-1]
        for font in self.display_fonts:
            if font.measure(text) <= width:
                selected = font
                break
        self.display_canvas.itemconfigure(self.display_text_id, text=text, font=selected)

    def _react_to_display(self, text: str, source: str) -> None:
        if not self.display_canvas:
            return
        canvas_width = max(self.display_canvas.winfo_width(), 360)
        right_edge = canvas_width - 16
        text_width = self.display_fonts[-1].measure(text)
        for font in self.display_fonts:
            if font.measure(text) <= canvas_width - 24:
                text_width = font.measure(text)
                break
        text_left = right_edge - text_width
        cat_width = len(CAT_SPRITES["idle"][0]) * PIXEL_SCALE

        if source == "result":
            perch = max(self.cat_min_x, min(self.cat_max_x, right_edge - min(text_width, 120)))
            self.cat_target_x = perch
            self.cat_state = "sleep"
            self.cat_sleep_ticks = 36
            return

        if source == "clear":
            self.cat_state = "idle"
            self.cat_push_ticks = 0
            self.cat_target_x = self.cat_min_x + 12
            return

        if text_left < self.cat_x + cat_width + 8:
            self.cat_target_x = max(self.cat_min_x, text_left - cat_width - 8)
            self.cat_push_ticks = 18
            self.cat_state = "idle"
        elif self.cat_push_ticks <= 0 and random.random() < 0.3:
            self.cat_target_x = random.uniform(self.cat_min_x + 10, self.cat_max_x - 10)

    def _on_display_resize(self, _: tk.Event) -> None:
        if not self.display_canvas or self.display_text_id is None:
            return
        w = self.display_canvas.winfo_width()
        h = self.display_canvas.winfo_height()
        self.cat_max_x = max(self.cat_min_x + 40, w - len(CAT_SPRITES["idle"][0]) * PIXEL_SCALE - 10)
        self.display_canvas.coords(self.display_text_id, w - 14, 34)
        self.display_canvas.coords("display-track", 12, h - 26, w - 12, h - 26)
        self._render_display_text(self.display_value.get())

    def _animate_cat(self) -> None:
        if not self.display_canvas:
            return

        self.cat_tick += 1
        floor_y = self.display_canvas.winfo_height() - 56
        sleep_y = 48

        if self.cat_state == "sleep" and self.cat_sleep_ticks > 0:
            self.cat_sleep_ticks -= 1
            self.cat_x += (self.cat_target_x - self.cat_x) * 0.25
            self.cat_y = sleep_y + (1 if (self.cat_tick // 8) % 2 else 0)
            pose = "sleep"
            if self.cat_sleep_ticks % 12 == 0:
                self.display_canvas.delete("cat-z")
                self.display_canvas.create_text(
                    self.cat_x + 30,
                    self.cat_y - 8,
                    text="zZ",
                    fill="#8D85A9",
                    font=("Segoe UI", 12, "bold"),
                    tags=("cat-z",),
                )
            elif self.cat_sleep_ticks % 4 == 0:
                self.display_canvas.delete("cat-z")
        else:
            self.display_canvas.delete("cat-z")
            self.cat_state = "idle"
            if self.cat_push_ticks > 0:
                self.cat_push_ticks -= 1
            elif abs(self.cat_x - self.cat_target_x) < 2 and self.cat_tick % 20 == 0:
                self.cat_target_x = random.uniform(self.cat_min_x + 8, self.cat_max_x - 8)

            step = 4.2 if self.cat_push_ticks > 0 else 2.2
            dx = self.cat_target_x - self.cat_x
            self.cat_x += max(-step, min(step, dx))
            self.cat_x = max(self.cat_min_x, min(self.cat_max_x, self.cat_x))
            self.cat_y = floor_y + (1 if (self.cat_tick // 6) % 2 else 0)
            if abs(dx) > 1.5:
                pose = "walk_a" if (self.cat_tick // 4) % 2 == 0 else "walk_b"
            else:
                pose = "blink" if self.cat_tick % 40 in {0, 1} else "idle"

        self._draw_cat(pose)
        self.root.after(90, self._animate_cat)

    def _draw_cat(self, pose: str) -> None:
        if not self.display_canvas:
            return
        self.display_canvas.delete("cat")
        sprite = CAT_SPRITES[pose]
        for py, row in enumerate(sprite):
            for px, char in enumerate(row):
                color = CAT_COLORS.get(char)
                if not color:
                    continue
                x0 = self.cat_x + px * PIXEL_SCALE
                y0 = self.cat_y + py * PIXEL_SCALE
                x1 = x0 + PIXEL_SCALE
                y1 = y0 + PIXEL_SCALE
                self.display_canvas.create_rectangle(
                    x0,
                    y0,
                    x1,
                    y1,
                    outline=color,
                    fill=color,
                    tags=("cat",),
                )
        self.display_canvas.tag_raise("cat")

    @staticmethod
    def _format_number(value: float) -> str:
        if float(value).is_integer():
            return str(int(value))
        return f"{value:.10g}"


def main() -> None:
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
