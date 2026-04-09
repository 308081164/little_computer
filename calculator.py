import math
import tkinter as tk
from tkinter import messagebox


BG = "#F4FDE6"
PANEL_BG = "#E8F7B6"
BTN_BG = "#D7F28A"
BTN_TEXT = "#1F4D1A"
OP_BG = "#A4D65E"
EQ_BG = "#4FAE4E"
DISPLAY_BG = "#FFF9C4"


class CalculatorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Little Computer")
        self.root.geometry("420x620")
        self.root.minsize(380, 560)
        self.root.configure(bg=BG)

        self.expression = ""
        self.display_value = tk.StringVar(value="0")

        self._build_ui()

    def _build_ui(self) -> None:
        frame = tk.Frame(self.root, bg=PANEL_BG, bd=0, highlightthickness=0)
        frame.pack(fill="both", expand=True, padx=14, pady=14)

        display = tk.Entry(
            frame,
            textvariable=self.display_value,
            font=("Segoe UI", 30, "bold"),
            justify="right",
            bd=0,
            bg=DISPLAY_BG,
            fg=BTN_TEXT,
            readonlybackground=DISPLAY_BG,
            relief="flat",
        )
        display.configure(state="readonly")
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=6, pady=(8, 16), ipady=18)

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
        self.display_value.set(self.expression or "0")

    def _clear_entry(self, _: str) -> None:
        self.expression = ""
        self.display_value.set("0")

    def _clear_all(self, _: str) -> None:
        self.expression = ""
        self.display_value.set("0")

    def _backspace(self, _: str) -> None:
        self.expression = self.expression[:-1]
        self.display_value.set(self.expression or "0")

    def _toggle_sign(self, _: str) -> None:
        if not self.expression:
            self.expression = "-"
        else:
            try:
                value = float(self.expression)
                self.expression = self._format_number(-value)
            except ValueError:
                self.expression = f"-({self.expression})"
        self.display_value.set(self.expression)

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
            self.display_value.set(self.expression)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("计算错误", str(exc))

    def _calculate(self, _: str) -> None:
        try:
            sanitized = self.expression.replace("×", "*").replace("÷", "/")
            result = eval(sanitized, {"__builtins__": {}}, {})
            self.expression = self._format_number(result)
            self.display_value.set(self.expression)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("计算错误", f"表达式无效: {exc}")

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
