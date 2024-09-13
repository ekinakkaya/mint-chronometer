import tkinter as tk
import time

class Chronometer:

    def __init__(self, root):
        self.root = root
        self.root.title("Mint")
        self.root.geometry("320x50")
        self.root.wm_attributes("-topmost", 1)
        self.root.resizable(False, False)
        self.root.overrideredirect(True)

        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        
        self.offset_x = 0
        self.offset_y = 0
        
        # main frame
        self.main_frame = tk.Frame(root, bg='lightgray')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # mouse events for moving the window
        self.main_frame.bind('<Button-1>', self.start_move)
        self.main_frame.bind('<B1-Motion>', self.do_move)

        # display
        self.label = tk.Label(self.main_frame, text="00:00:00", font=("Arial", 26), bg='lightgray')
        self.label.pack(side=tk.LEFT, padx=5)
        
        # buttons
        self.button_frame = tk.Frame(self.main_frame, bg='lightgray')
        self.button_frame.pack(side=tk.RIGHT)

        self.start_stop_button = tk.Button(self.button_frame, text="⏵", font=("Arial", 14), command=self.start_stop, width=3)
        self.start_stop_button.pack(side=tk.LEFT, padx=2)

        self.reset_button = tk.Button(self.button_frame, text="🔄", font=("Arial", 14), command=self.reset, width=3)
        self.reset_button.pack(side=tk.LEFT, padx=2)

        self.exit_button = tk.Button(self.button_frame, text="   X️", font=("Arial", 14), command=self.exit_app, width=3)
        self.exit_button.pack(side=tk.LEFT, padx=2)
        
        self.update_clock()

    # movements
    def start_move(self, event):
        # start the movement of the window
        self.offset_x = event.x
        self.offset_y = event.y

    def do_move(self, event):
        # actual moving of the window
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f'+{x}+{y}')

    def update_clock(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.update_label()

        if self.window_handle is not None:
            win32gui.SetWindowPos(self.window_handle, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        self.root.after(50, self.update_clock)
        
    def update_label(self):
        minutes, seconds = divmod(int(self.elapsed_time), 60)
        hours, minutes = divmod(minutes, 60)
        self.label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")
    
    def start_stop(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.start_stop_button.config(text="⏸")
        else:
            self.running = False
            self.start_stop_button.config(text="⏵")
    
    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.update_label()
        self.start_stop_button.config(text="⏵")
    
    def exit_app(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    chronometer = Chronometer(root)
    root.mainloop()