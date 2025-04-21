import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, INFO, HORIZONTAL, BOTH
from PIL import Image, ImageTk
import os
from watermarkLogic import WatermarkLogic
import time

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermark App")
        self.root.geometry("500x640")

        self.primary_color = "#4A90E2"
        self.neutral_bg = "#F5F7FA"
        self.text_color = "#2D3436"

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Open Sans", 10), foreground=self.text_color)
        self.style.configure("TButton", font=("Open Sans", 9), padding=5)
        self.style.map("TButton", background=[("active", "#5DADE2")])
        self.style.configure("TEntry", padding=5)
        self.style.configure("TCombobox", padding=5)
        self.style.configure("TFrame", background=self.neutral_bg)

        self.watermark_logic = WatermarkLogic()

        self.setup_ui()
        self.load_default_preferences()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=BOTH, expand=True)

        ttk.Label(self.main_frame, text="Watermark Your Image", font=("Open Sans", 14, "bold")).pack(pady=(0, 5))

        self.image_frame = ttk.Frame(self.main_frame)
        self.image_frame.pack(fill="x", pady=5)
        self.select_button = ttk.Button(self.image_frame, text="Select Image", command=self.select_image, bootstyle=PRIMARY)
        self.select_button.pack(side="left", padx=2)
        self.image_label = ttk.Label(self.image_frame, text="No image selected")
        self.image_label.pack(side="left", padx=2)
        self.image_thumbnail = ttk.Label(self.image_frame)
        self.image_thumbnail.pack(side="left", padx=2)

        self.text_frame = ttk.Frame(self.main_frame)
        self.text_frame.pack(fill="x", pady=5)
        ttk.Label(self.text_frame, text="Watermark Text:", font=("Open Sans", 10, "bold")).pack(anchor="w")
        self.watermark_entry = ttk.Entry(self.text_frame, width=40)
        self.watermark_entry.pack(pady=2, fill="x")

        self.style_frame = ttk.Frame(self.main_frame)
        self.style_frame.pack(fill="x", pady=5)
        ttk.Label(self.style_frame, text="Watermark Style:", font=("Open Sans", 10, "bold")).pack(anchor="w")
        self.watermark_type = tk.StringVar()
        ttk.Radiobutton(self.style_frame, text="Text Watermark", variable=self.watermark_type, value="Text").pack(anchor="w", pady=1)
        ttk.Radiobutton(self.style_frame, text="Image Watermark", variable=self.watermark_type, value="Image").pack(anchor="w", pady=1)
        self.image_watermark_button = ttk.Button(self.style_frame, text="Select Watermark Image", command=self.select_watermark_image, state="disabled")
        self.image_watermark_button.pack(anchor="w", pady=1)
        self.watermark_type.trace("w", self.toggle_watermark_type)

        self.position_frame = ttk.Frame(self.main_frame)
        self.position_frame.pack(fill="x", pady=5)
        ttk.Label(self.position_frame, text="Watermark Position:", font=("Open Sans", 10, "bold"), foreground=self.text_color).pack(anchor="w")
        self.position_var = tk.StringVar()
        positions = ["Top Left", "Top Center", "Top Right", "Center Left", "Center", "Center Right", "Bottom Left", "Bottom Center", "Bottom Right"]
        self.position_menu = ttk.Combobox(self.position_frame, textvariable=self.position_var, values=positions, state="readonly")
        self.position_menu.pack(pady=2, fill="x")

        self.font_frame = ttk.Frame(self.main_frame)
        self.font_frame.pack(fill="x", pady=5)
        self.font_label = ttk.Label(self.font_frame, text="Font Settings:", font=("Open Sans", 10, "bold"), foreground=self.text_color)
        self.font_label.pack(anchor="w")
        self.font_var = tk.StringVar()
        fonts = ["Arial", "Times New Roman", "Courier New"]
        self.font_menu = ttk.Combobox(self.font_frame, textvariable=self.font_var, values=fonts, state="readonly")
        self.font_menu.pack(pady=2, fill="x")
        self.font_size = tk.IntVar()
        self.font_size_label = ttk.Label(self.font_frame, text=f"Font Size: {self.font_size.get()}")
        self.font_size_label.pack(anchor="w")
        self.font_slider = ttk.Scale(self.font_frame, from_=10, to=100, orient=HORIZONTAL, variable=self.font_size)
        self.font_slider.pack(pady=2, fill="x")
        self.font_size.trace("w", self.update_font_label)

        self.opacity_frame = ttk.Frame(self.main_frame)
        self.opacity_frame.pack(fill="x", pady=5)
        ttk.Label(self.opacity_frame, text="Opacity & Color:", font=("Open Sans", 10, "bold"), foreground=self.text_color).pack(anchor="w")
        self.opacity = tk.IntVar()
        self.opacity_label = ttk.Label(self.opacity_frame, text=f"Watermark Opacity (%): {self.opacity.get()}")
        self.opacity_label.pack(anchor="w")
        self.opacity_slider = ttk.Scale(self.opacity_frame, from_=0, to=100, orient=HORIZONTAL, variable=self.opacity)
        self.opacity_slider.pack(pady=2, fill="x")
        self.opacity.trace("w", self.update_opacity_label)
        self.color = "white"
        self.color_frame = ttk.Frame(self.opacity_frame)
        self.color_frame.pack(fill="x", pady=2)
        self.color_button = ttk.Button(self.color_frame, text="Choose Watermark Color", command=self.choose_color, bootstyle=INFO)
        self.color_button.pack(side="left", padx=2)
        self.color_display = tk.Canvas(self.color_frame, width=20, height=20, bg="white", highlightthickness=1, highlightbackground=self.text_color)
        self.color_display.pack(side="left")

        self.action_frame = ttk.Frame(self.main_frame)
        self.action_frame.pack(fill="x", pady=5)
        self.preview_button = ttk.Button(self.action_frame, text="Preview Watermark", command=self.preview_watermark, style="Accent.TButton")
        self.preview_button.pack(side="left", padx=2, fill="x", expand=True)
        self.apply_button = ttk.Button(self.action_frame, text="Apply and Save", command=self.apply_watermark, style="Accent.TButton")
        self.apply_button.pack(side="left", padx=2, fill="x", expand=True)

    def toggle_watermark_type(self, *args):
        if self.watermark_type.get() == "Image":
            self.image_watermark_button.configure(state="normal")
            self.font_menu.configure(state="disabled")
            self.font_slider.configure(state="disabled")
        else:
            self.image_watermark_button.configure(state="disabled")
            self.font_menu.configure(state="normal")
            self.font_slider.configure(state="normal")

    def update_font_label(self, *args):
        self.font_size_label.config(text=f"Font Size: {int(self.font_size.get())}")

    def update_opacity_label(self, *args):
        self.opacity_label.config(text=f"Watermark Opacity (%): {int(self.opacity.get())}")

    def select_image(self):
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        self.image_path = filedialog.askopenfilename(filetypes=filetypes)
        if self.image_path:
            self.image_label.config(text=os.path.basename(self.image_path))
            try:
                self.image = Image.open(self.image_path).convert("RGBA")
                thumb = self.image.copy()
                thumb.thumbnail((40, 40))
                self.image_thumb = ImageTk.PhotoImage(thumb)
                self.image_thumbnail.config(image=self.image_thumb)
            except Exception:
                messagebox.showerror("Error", "Invalid image file!", parent=self.root)
                self.image_path = None
                self.image = None
                self.image_label.config(text="No image selected")
                self.image_thumbnail.config(image="")

    def select_watermark_image(self):
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        self.watermark_image_path = filedialog.askopenfilename(filetypes=filetypes)
        if self.watermark_image_path:
            try:
                self.watermark_image = Image.open(self.watermark_image_path).convert("RGBA")
            except Exception:
                messagebox.showerror("Error", "Invalid watermark image!", parent=self.root)
                self.watermark_image_path = None
                self.watermark_image = None

    def choose_color(self):
        color = tk.colorchooser.askcolor(title="Choose Watermark Color", parent=self.root)[1]
        if color:
            self.color = color
            self.color_display.delete("all")
            self.color_display.create_rectangle(0, 0, 20, 20, fill=color, outline=self.text_color)

    def preview_watermark(self):
        if not hasattr(self, "image_path") or not self.image_path or not self.image:
            messagebox.showwarning("Warning", "Please select an image first!", parent=self.root)
            return
        if self.watermark_type.get() == "Text":
            text = self.watermark_entry.get()
            if not text:
                messagebox.showwarning("Warning", "Please enter watermark text!", parent=self.root)
                return
            watermark_image = None
        else:
            if not hasattr(self, "watermark_image") or not self.watermark_image:
                messagebox.showwarning("Warning", "Please select a watermark image!", parent=self.root)
                return
            text = ""
            watermark_image = self.watermark_image

        watermarked = self.watermark_logic.add_watermark(
            self.image,
            text,
            self.position_var.get(),
            self.font_size.get(),
            self.color,
            self.font_var.get(),
            self.opacity.get(),
            watermark_image
        )

        preview_image = watermarked.convert("RGB")
        preview_image.thumbnail((250, 250))
        photo = ImageTk.PhotoImage(preview_image)

        preview_window = ttk.Toplevel(self.root)
        preview_window.title("Watermark Preview")
        preview_label = ttk.Label(preview_window, image=photo)
        preview_label.pack(pady=5)
        preview_window.photo = photo

        for alpha in range(0, 255, 10):
            preview_window.attributes("-alpha", alpha / 255)
            preview_window.update()
            time.sleep(0.02)

    def apply_watermark(self):
        if not hasattr(self, "image_path") or not self.image_path or not self.image:
            messagebox.showwarning("Warning", "Please select an image first!", parent=self.root)
            return
        if self.watermark_type.get() == "Text":
            text = self.watermark_entry.get()
            if not text:
                messagebox.showwarning("Warning", "Please enter watermark text!", parent=self.root)
                return
            watermark_image = None
        else:
            if not hasattr(self, "watermark_image") or not self.watermark_image:
                messagebox.showwarning("Warning", "Please select a watermark image!", parent=self.root)
                return
            text = ""
            watermark_image = self.watermark_image

        watermarked = self.watermark_logic.add_watermark(
            self.image,
            text,
            self.position_var.get(),
            self.font_size.get(),
            self.color,
            self.font_var.get(),
            self.opacity.get(),
            watermark_image
        )

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            initialfile=os.path.splitext(os.path.basename(self.image_path))[0] + "_watermarked"
        )
        if save_path:
            try:
                watermarked.save(save_path)
                messagebox.showinfo("Success", "Watermarked image saved successfully!", parent=self.root, icon="info")
                # Removed the save_preferences call
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}", parent=self.root)

    def load_default_preferences(self):
        default_prefs = {
            "watermark_text": "Your Watermark",
            "position": "Bottom Right",
            "font": "Arial",
            "font_size": 30,
            "opacity": 80,
            "color": "white",
            "watermark_type": "Text"
        }
        self.watermark_entry.delete(0, tk.END)
        self.watermark_entry.insert(0, default_prefs["watermark_text"])
        self.position_var.set(default_prefs["position"])
        self.font_var.set(default_prefs["font"])
        self.font_size.set(default_prefs["font_size"])
        self.opacity.set(default_prefs["opacity"])
        self.color = default_prefs["color"]
        self.color_display.delete("all")
        self.color_display.create_rectangle(0, 0, 20, 20, fill=self.color, outline=self.text_color)
        self.watermark_type.set(default_prefs["watermark_type"])
        self.update_font_label()
        self.update_opacity_label()

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    root.configure(bg="#F5F7FA")
    app = WatermarkApp(root)
    root.mainloop()