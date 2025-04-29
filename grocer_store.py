import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import tempfile
import os
import win32api
import win32print

# Product data
products = {
    "Maggie": {"price": 80, "image": r"D:\Degree\final_Python_prj\images\maggie.PNG"},
    "Noodles": {"price": 100, "image": r"D:\Degree\final_Python_prj\images\noodles.PNG"},
    "Rice": {"price": 400, "image": r"D:\Degree\final_Python_prj\images\rice.PNG"},
    "Biscuits": {"price": 30, "image": r"D:\Degree\final_Python_prj\images\biscuits.PNG"}
}

# Shopping cart
cart = {}

def add_to_cart(product, qty_var):
    qty = int(qty_var.get())
    if qty > 0:
        if product in cart:
            cart[product] += qty
        else:
            cart[product] = qty
        messagebox.showinfo("Success", f"Added {qty} {product}(s) to cart.")

def view_cart():
    top = tk.Toplevel(root)
    top.title("View Cart")
    total = 0
    row = 0

    for product, qty in cart.items():
        item = products[product]
        price = item["price"]
        subtotal = qty * price
        total += subtotal

        image = Image.open(item["image"]).resize((100, 100))
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(top, image=photo)
        label.image = photo
        label.grid(row=row, column=0, padx=10, pady=10)

        tk.Label(top, text=f"{product}").grid(row=row, column=1)
        tk.Label(top, text=f"Qty: {qty}").grid(row=row, column=2)
        tk.Label(top, text=f"Rs. {subtotal}").grid(row=row, column=3)
        row += 1

    tk.Label(top, text=f"Total: Rs. {total}", font=("Arial", 14, "bold")).grid(row=row, columnspan=4, pady=10)

def generate_invoice():
    try:
        file_path = tempfile.mktemp(".pdf")
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y = height - 50
        total = 0

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Invoice")
        y -= 40

        for product, qty in cart.items():
            item = products[product]
            price = item["price"]
            subtotal = qty * price
            total += subtotal

            # Draw product image
            try:
                img_reader = ImageReader(item["image"])
                c.drawImage(img_reader, 50, y - 60, width=50, height=50)
            except Exception as e:
                print(f"Image load error for {product}: {e}")

            # Draw text next to image
            c.setFont("Helvetica", 12)
            c.drawString(120, y - 10, f"{product} - Qty: {qty} - Rs. {subtotal}")
            y -= 70
            if y < 100:
                c.showPage()
                y = height - 50

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, f"Total Bill: Rs. {total}")
        c.save()

        win32api.ShellExecute(0, "print", file_path, None, ".", 0)
        messagebox.showinfo("Success", "Invoice sent to printer.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to print invoice:\n{e}")

def go_to_shop():
    # Destroy the main screen and open the grocery shop window
    main_screen.destroy()
    open_grocery_shop()

def open_grocery_shop():
    global root
    # This is your existing grocery shop window code
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.title("Grocery Store")

    # Background Image
    bg_img = Image.open(r"D:\Degree\final_Python_prj\images\bg.png").resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    bg_photo = ImageTk.PhotoImage(bg_img)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Product Display Frame with Scrollbar
    frame = tk.Frame(root, bg="white")
    frame.pack(pady=50)

    canvas_main = tk.Canvas(frame, width=1000, height=500, bg="white")
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas_main.yview)
    scrollable_frame = tk.Frame(canvas_main, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas_main.configure(scrollregion=canvas_main.bbox("all"))
    )

    canvas_main.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas_main.configure(yscrollcommand=scrollbar.set)

    canvas_main.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Product Display
    col = 0
    for product, info in products.items():
        img = Image.open(info["image"]).resize((150, 150))
        photo = ImageTk.PhotoImage(img)

        item_frame = tk.Frame(scrollable_frame, bg="white", padx=20, pady=20)
        item_frame.grid(row=0, column=col)

        img_label = tk.Label(item_frame, image=photo)
        img_label.image = photo
        img_label.pack()

        tk.Label(item_frame, text=product, font=("Arial", 14)).pack()
        tk.Label(item_frame, text=f"Rs. {info['price']}", font=("Arial", 12)).pack()

        qty_var = tk.StringVar(value="1")
        tk.Entry(item_frame, textvariable=qty_var, width=5).pack(pady=5)
        tk.Button(item_frame, text="Add to Cart", command=lambda p=product, q=qty_var: add_to_cart(p, q)).pack()

        col += 1

    # Bottom Buttons
    btn_frame = tk.Frame(root, bg="white")
    btn_frame.pack(pady=20)

    tk.Button(btn_frame, text="View Cart", font=("Arial", 14), command=view_cart).pack(side="left", padx=20)
    tk.Button(btn_frame, text="Generate Invoice", font=("Arial", 14), command=generate_invoice).pack(side="left", padx=20)
    tk.Button(btn_frame, text="Exit", font=("Arial", 14), command=root.quit).pack(side="left", padx=20)

    root.mainloop()

# ------------------- Main Screen -------------------
main_screen = tk.Tk()
main_screen.attributes('-fullscreen', True)
main_screen.title("Welcome to Grocery Store")

# Background Image for Main Screen
bg_img = Image.open(r"D:\Degree\final_Python_prj\images\bg.png").resize((main_screen.winfo_screenwidth(), main_screen.winfo_screenheight()))
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(main_screen, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Welcome Message
welcome_label = tk.Label(main_screen, text="Welcome to Grocery Store", font=("Arial", 36, "bold"), bg="white", fg="green")
welcome_label.pack(pady=100)

# Button to go to the shop
go_to_shop_button = tk.Button(main_screen, text="Go to the Grocery Shop", font=("Arial", 18), command=go_to_shop)
go_to_shop_button.pack(pady=20)

main_screen.mainloop()





























