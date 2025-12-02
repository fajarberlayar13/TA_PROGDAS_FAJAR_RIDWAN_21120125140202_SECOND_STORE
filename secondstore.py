import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk


# ===================================================
# CLASS PRODUK
# ===================================================
class Product:
    def __init__(self, name, price, category, desc, image):
        self.name = name
        self.price = price
        self.category = category
        self.desc = desc
        self.image = image


class Electronics(Product):
    def __init__(self, name, price, desc, warranty, image):
        super().__init__(name, price, "Elektronik", desc, image)
        self.warranty = warranty



# ===================================================
# HALAMAN UTAMA SECOND STORE
# ===================================================
class SecondStoreApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Second Store")
        self.master.geometry("520x650")
        
        self.colors = {
            'bg': '#F5F7FA',
            'primary': '#4A90E2',
            'secondary': '#50C878',
            'accent': '#FF6B6B',
            'text': '#2C3E50',
            'card': '#FFFFFF',
            'border': '#E1E8ED'
        }
        
        self.master.configure(bg=self.colors['bg'])

        # DATA PRODUK
        self.products = [
            Product("Sepatu Bekas", 150000, "Fashion", "Masih bagus, jarang dipakai", "sepatu.png"),
            Electronics("Laptop Bekas", 2500000, "Core i5, 8GB RAM", "1 bulan", "laptop.png"),
            Product("Meja Belajar", 200000, "Furniture", "Kayu kuat", "meja.png"),
            Product("Tas Gunung Bekas", 180000, "Outdoor", "Kondisi 90%", "tas.png"),
            Electronics("Kamera Bekas", 850000, "Masih normal semua fitur", "3 minggu", "kamera.png")
        ]

        self.history_stack = []
        self.cart = []  # STACK

        # ---------------------- HEADER ----------------------
        header_frame = tk.Frame(master, bg=self.colors['card'], relief=tk.FLAT, bd=0)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        self.title_label = tk.Label(
            header_frame, 
            text="🛍️ Second Store", 
            font=("Segoe UI", 24, "bold"),
            bg=self.colors['card'],
            fg=self.colors['primary']
        )
        self.title_label.pack(pady=15)
        
        subtitle = tk.Label(
            header_frame,
            text="Temukan barang bekas berkualitas dengan harga terjangkau",
            font=("Segoe UI", 9),
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        subtitle.pack(pady=(0, 15))

        # ---------------------- LIST PRODUK ----------------------
        list_frame = tk.Frame(master, bg=self.colors['card'], relief=tk.FLAT, bd=1)
        list_frame.pack(padx=15, pady=(0, 15), fill=tk.BOTH, expand=True)
        
        list_label = tk.Label(
            list_frame,
            text="📦 Daftar Produk",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text'],
            anchor="w"
        )
        list_label.pack(padx=15, pady=(12, 8), fill=tk.X)

        self.listbox = tk.Listbox(
            list_frame, width=45, height=10,
            font=("Segoe UI", 10),
            bg='#FFFFFF', fg=self.colors['text'],
            selectbackground=self.colors['primary'],
            selectforeground='#FFFFFF',
            relief=tk.FLAT, bd=0,
            highlightthickness=1,
            highlightcolor=self.colors['primary'],
            highlightbackground=self.colors['border']
        )
        self.listbox.pack(padx=15, pady=(0, 15), fill=tk.BOTH, expand=True)

        for p in self.products:
            self.listbox.insert(tk.END, f"  {p.name} - Rp{p.price:,}")

        # ---------------------- BUTTON AREA ----------------------
        btn_frame = tk.Frame(master, bg=self.colors['bg'])
        btn_frame.pack(pady=15, padx=15)

        button_style = {
            'font': ('Segoe UI', 10, 'bold'),
            'relief': tk.FLAT,
            'bd': 0,
            'cursor': 'hand2',
            'padx': 20,
            'pady': 12,
            'width': 16
        }

        self.btn_detail = tk.Button(
            btn_frame, text="👁️ Lihat Detail",
            command=self.show_detail,
            bg=self.colors['primary'],
            fg='navy',
            activebackground="#357ABD",
            activeforeground="#FFFFFF",
            **button_style
        )
        self.btn_detail.grid(row=0, column=0, padx=8, pady=8)

        self.btn_add_cart = tk.Button(
            btn_frame, text="🛒 Tambah ke Keranjang",
            command=self.add_to_cart,
            bg=self.colors['secondary'],
            fg="navy",
            activebackground="#3EA76A",
            activeforeground="#FFFFFF",
            **button_style
        )
        self.btn_add_cart.grid(row=0, column=1, padx=8, pady=8)

        self.btn_cart = tk.Button(
            btn_frame, text="🧺 Lihat Keranjang",
            command=self.show_cart,
            bg='#9B59B6',
            fg='navy',
            activebackground="#8E44AD",
            activeforeground="#FFFFFF",
            **button_style
        )
        self.btn_cart.grid(row=1, column=0, padx=8, pady=8)

        self.btn_checkout = tk.Button(
            btn_frame, text="✔ Checkout",
            command=self.checkout,
            bg=self.colors['accent'],
            fg='navy',
            activebackground="#E85C5C",
            activeforeground="#FFFFFF",
            **button_style
        )
        self.btn_checkout.grid(row=1, column=1, padx=8, pady=8)

        self.btn_history = tk.Button(
            btn_frame, text="📜 History",
            command=self.show_history,
            bg='#2C3E50',
            fg='navy',
            activebackground="#1A252F",
            activeforeground="#FFFFFF",
            **button_style
        )
        self.btn_history.grid(row=2, column=0, padx=8, pady=8)


    # ===================================================
    # DETAIL PRODUK
    # ===================================================
    def show_detail(self):
        index = self.listbox.curselection()
        if not index:
            messagebox.showwarning("Warning", "Pilih produk terlebih dahulu!")
            return

        product = self.products[index[0]]
        self.history_stack.append(product.name)

        detail_win = tk.Toplevel(self.master)
        detail_win.title(f"Detail - {product.name}")
        detail_win.geometry("400x520")
        detail_win.configure(bg=self.colors['bg'])

        header_card = tk.Frame(detail_win, bg=self.colors['card'])
        header_card.pack(fill=tk.X, padx=15, pady=15)

        title_detail = tk.Label(
            header_card,
            text="📋 Detail Produk",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['card'],
            fg=self.colors['primary']
        )
        title_detail.pack(pady=12)

        img_frame = tk.Frame(detail_win, bg=self.colors['card'])
        img_frame.pack(padx=15, pady=(0, 15), fill=tk.X)
        
        try:
            img = Image.open(product.image)
            img = img.resize((220, 220), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)

            img_label = tk.Label(img_frame, image=img, bg=self.colors['card'])
            img_label.image = img
            img_label.pack(pady=15)
        except:
            tk.Label(img_frame, text="Gambar tidak tersedia").pack()

        info_frame = tk.Frame(detail_win, bg=self.colors['card'])
        info_frame.pack(padx=15, pady=(0, 15), fill=tk.BOTH, expand=True)
        
        info_text = f"Nama: {product.name}\nHarga: Rp{product.price:,}\nKategori: {product.category}\nDeskripsi: {product.desc}"

        if isinstance(product, Electronics):
            info_text += f"\nGaransi: {product.warranty}"

        tk.Label(info_frame, text=info_text, bg=self.colors['card'], justify="left").pack(padx=20, pady=20)


    # ===================================================
    # KERANJANG (STACK)
    # ===================================================
    def add_to_cart(self):
        index = self.listbox.curselection()
        if not index:
            messagebox.showwarning("Warning", "Pilih produk dulu!")
            return

        product = self.products[index[0]]
        self.cart.append(product)
        messagebox.showinfo("Berhasil", f"{product.name} masuk ke keranjang!")

    def show_cart(self):
        if not self.cart:
            messagebox.showinfo("Keranjang", "Keranjang masih kosong.")
            return
        
        cart_text = "\n".join([f"- {p.name} (Rp{p.price:,})" for p in self.cart])
        messagebox.showinfo("🧺 Keranjang Belanja", cart_text)


    # ===================================================
    # CHECKOUT
    # ===================================================
    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Checkout", "Keranjang kosong!")
            return
        
        total = sum(p.price for p in self.cart)
        
        confirm = messagebox.askyesno(
            "Checkout",
            f"Total belanja: Rp{total:,}\n\nYakin ingin checkout?"
        )

        if confirm:
            self.cart.clear()
            messagebox.showinfo("Sukses", "Checkout berhasil!")


    # ===================================================
    # HISTORY (STACK)
    # ===================================================
    def show_history(self):
        if not self.history_stack:
            messagebox.showinfo("History", "Belum ada history.")
        else:
            history_text = "\n".join(reversed(self.history_stack))
            messagebox.showinfo("History Produk Dibuka", history_text)



# ===================================================
# MENU AWAL (START MENU)
# ===================================================
class StartMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Second Store - Menu Awal")
        self.master.geometry("420x300")
        self.master.configure(bg="#F5F7FA")

        title = tk.Label(
            master,
            text="Selamat Datang di Second Store",
            font=("Segoe UI", 18, "bold"),
            bg="#F5F7FA",
            fg="#4A90E2"
        )
        title.pack(pady=40)

        # Tombol START — warna biru
        btn_start = tk.Button(
            master,
            text="🚀 Mulai Aplikasi",
            font=("Segoe UI", 12, "bold"),
            width=20,
            bg="#4A90E2",
            fg="navy",
            activebackground="#357ABD",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            bd=0,
            pady=10,
            command=self.open_app
        )
        btn_start.pack(pady=15)

        # Tombol EXIT — warna merah
        btn_exit = tk.Button(
            master,
            text="❌ Keluar",
            font=("Segoe UI", 12, "bold"),
            width=20,
            bg="#FF6B6B",
            fg="red",
            activebackground="#E84C4C",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            bd=0,
            pady=10,
            command=self.master.destroy
        )
        btn_exit.pack(pady=10)

    def open_app(self):
        self.master.destroy()

        root = tk.Tk()
        SecondStoreApp(root)
        root.mainloop()


# ===================================================
# RUN PROGRAM — mulai dari MENU AWAL
# ===================================================
root = tk.Tk()
StartMenu(root)
root.mainloop()
