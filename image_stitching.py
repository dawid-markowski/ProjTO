import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

#image_paths=['images/karmel/carmel-00.png','images/karmel/carmel-01.png','images/karmel/carmel-02.png','images/karmel/carmel-03.png','images/karmel/carmel-04.png']
#image_paths=['images/diamondhead/diamondhead-10.png','images/diamondhead/diamondhead-11.png','images/diamondhead/diamondhead-12.png','images/diamondhead/diamondhead-13.png']
#image_paths=['images/hotel/hotel-02.png','images/hotel/hotel-03.png','images/hotel/hotel-04.png']
#image_paths=['images/rio/rio-47.png','images/rio/rio-48.png','images/rio/rio-49.png']
#image_paths=['images/golden/goldengate-00.png','images/golden/goldengate-01.png','images/golden/goldengate-02.png','images/golden/goldengate-03.png','images/golden/goldengate-04.png','images/golden/goldengate-05.png']


# Funkcja do wczytywania obrazów
def load_images():
    global image_paths
    image_paths = filedialog.askopenfilenames(
        title="Wybierz obrazy",
        filetypes=[("Pliki obrazów", "*.png *.jpg *.jpeg *.bmp")]
    )
    if image_paths:
        messagebox.showinfo("Informacja", f"Załadowano {len(image_paths)} obrazów.")
    else:
        messagebox.showerror("Błąd", "Nie wybrano żadnych obrazów.")

def create_panorama():
	if not image_paths:
		messagebox.showerror("Błąd", "Najpierw wczytaj obrazy!")
		return

	imgs = []
	for i in image_paths:
		img = cv2.imread(i)
		img = cv2.resize(img, (0, 0), fx=1, fy=1) #Ewentualne skalowanie obrazków gdy jest ich za dużo
		imgs.append(img)

	stitcher = cv2.Stitcher.create()
	(status, panorama) = stitcher.stitch(imgs)

	if status != cv2.STITCHER_OK:
		messagebox.showerror("Błąd", "Tworzenie panoramy nie powiodło się.")
		return

	# Wypełnianie czarnych obszarów
	panorama_finished = remove_black_borders(panorama)

	# Zapisanie i wyświetlenie panoramy
	cv2.imwrite("panorama_result.png", panorama_finished)
	display_image("panorama_result.png")
	messagebox.showinfo("Panorama gotowa!!!", "Panorama została zapisana jako 'panorama_result.png'.")


def remove_black_borders(image):
	# Tworzenie maski czarnych obszarów
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY_INV)[1]

	# Wypełnianie czarnych obszarów
	blackremoved_image = cv2.inpaint(image, mask, inpaintRadius=20, flags=cv2.INPAINT_TELEA)
	return blackremoved_image


# Funkcja do wyświetlania obrazu w GUI
def display_image(image_path):
	img = Image.open(image_path)
	img.thumbnail((800, 600))  # Dopasowanie rozmiaru do GUI
	img = ImageTk.PhotoImage(img)

	panel.config(image=img)
	panel.image = img

# Główne okno GUI
root = tk.Tk()
root.title("Tworzenie Panoramy")
root.geometry("1000x700")

# Elementy GUI
frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Wybierz obrazy do stworzenia panoramy:", font=("Arial", 24)).pack(pady=7)
button1 = tk.Button(frame, text="Wczytaj obrazy", command=load_images, font=("Arial", 16), width=20, height=2, bg="gray", fg="black")
button1.pack(pady=10)

button2 = tk.Button(frame, text="Stwórz panoramę", command=create_panorama, font=("Arial", 16), width=20, height=2, bg="gray", fg="black")
button2.pack(pady=10)

panel = ttk.Label(frame)
panel.pack(pady=10)

# Start aplikacji
image_paths = []
root.mainloop()
