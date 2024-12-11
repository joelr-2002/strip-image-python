import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

def load_image():
    global original_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        try:
            original_image = Image.open(file_path)
            image_label.config(text=f"Imagen cargada: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open image.\n{e}")

def execute():
    if original_image:
        try:
            num_phases = phases_scale.get()
            base_size = (150, 150)
            phases = [original_image.resize(base_size, Image.LANCZOS) for _ in range(num_phases)]
            strip_width = base_size[0] * num_phases
            strip_height = base_size[1]
            strip = Image.new("RGBA", (strip_width, strip_height))

            for idx, phase in enumerate(phases):
                strip.paste(phase, (idx * base_size[0], 0))

            save_image(strip)
        except Exception as e:
            messagebox.showerror("Error", f"Error processing image.\n{e}")
    else:
        messagebox.showwarning("Warning", "Please load an image first.")

def save_image(strip):
    dir_path = filedialog.askdirectory()
    if dir_path:
        file_path = f"{dir_path}/catedral_evolution_strip.png"
        strip.save(file_path)
        messagebox.showinfo("Success", f"Image saved to {file_path}")

# Initialize the main application window
root = tk.Tk()
root.title("Image Evolution Strip")
root.geometry("300x300")  # Set initial window size to 300x300 pixels

original_image = None

# Create and place the load button
load_button = tk.Button(root, text="Load Image", command=load_image)
load_button.pack(pady=10)

# Label to show image load status
image_label = tk.Label(root, text="No image loaded")
image_label.pack(pady=5)

# Create and place a scale to select the number of strips
phases_scale = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, label="Number of Phases")
phases_scale.set(5)
phases_scale.pack(pady=10)

# Create and place the execute button
execute_button = tk.Button(root, text="Generate and Save", command=execute)
execute_button.pack(pady=10)

# Create and place the label to display the output image
output_label = tk.Label(root)
output_label.pack(pady=10)

# Run the application
root.mainloop()
