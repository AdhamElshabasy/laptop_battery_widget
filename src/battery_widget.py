# Importing modules and libraries
import psutil
import customtkinter
from datetime import datetime

# App UI class inheriting from customTkinter


class BatteryWidget(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        # Setting the widget title
        self.title("Battery Status")
        # Making the widget non-resizable
        self.resizable(False, False)
        # Setting the background
        self.config(bg='black')
        # Make the window stay on top
        self.wm_attributes("-topmost", 1)
        # Remove the title bar
        self.overrideredirect(True)

        # Flag to check if the charger was disconnected only one time
        self.disconnect_flag = True
        # Variables to store the percentage and time
        self.disconnect_per = 0
        self.disconnect_time = datetime.now()

        self.battery_percentage = 0
        self.battery_plugged = True
        self.battery_seconds_left = 0

        # Call the function that creates the widgets
        self.create_widgets()
        # Call the function that updates the data in the widget
        self.update_data()
        # Call the update data function
        self.get_info()

    # Get the position of the mouse

    def get_pos(self, event):

        self.xwin = event.x
        self.ywin = event.y

    # Move the window with the mouse coordinates
    def move_window(self, event):
        self.geometry(
            f'+{event.x_root - self.xwin}+{event.y_root - self.ywin}')

    # Function returning time in hh:mm:ss
    def convert_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "%d:%02d:%02d" % (hours, minutes, seconds)

    # Function to close the program
    def close(self):
        self.quit()

    # Change the text and color according to status
    def change_status(self, main_color, charger_color, charger_text):

        # Set the main color of the widget
        self.laptop_percentage.configure(text_color=main_color)
        self.percentage_progressbar.configure(progress_color=main_color)
        self.eta_time.configure(text_color=main_color)
        self.elapsed_time.configure(text_color=main_color)

        # Set the charger status label color and text
        self.charger_status.configure(text_color=charger_color)
        self.charger_status.configure(text=charger_text)

        # Display Time remaining if found
        if self.battery_seconds_left < 40000 and self.battery_plugged == False:
            self.eta_time.configure(
                text=f"Time Remaining: {self.convert_time(self.battery_seconds_left)}")

    # Function to update the data
    def get_info(self):

        # Get the data from the sensor
        battery = psutil.sensors_battery()

        # Set the values of the variables
        self.battery_percentage = battery.percent
        self.battery_plugged = battery.power_plugged
        self.battery_seconds_left = battery.secsleft

        # If the charger is plugged in
        if battery.power_plugged:

            # indicate that the charger was connected and reset indicators
            self.disconnect_flag = True
            self.disconnect_per = 0

        # If the charger is NOT plugged in
        else:

            # If the charger just disconnected
            if self.disconnect_flag:
                # Get the time and percentage and close the flag
                self.disconnect_per = battery.percent
                self.disconnect_time = datetime.now()
                self.disconnect_flag = False

    # Function that updates the data every second
    def update_data(self):

        # Update the data in the GetBatteryInfo class
        self.get_info()

        # Display the percentage on the label
        self.laptop_percentage.configure(
            text=f"Battery Level: {self.battery_percentage}%")

        # Set the percentage of the progressbar
        self.percentage_progressbar.set(
            self.battery_percentage / 100)

        # If the charger is plugged in...
        if self.battery_plugged:

            # Display No time
            self.eta_time.configure(text=f"Time Remaining: _ : _ : _")

            # If charged to 100%...
            if self.battery_percentage == 100:
                # Set the colors and text accordingly
                self.change_status("#00ffc8", "#00ffc8", "Fully Charged")

            # If still charging...
            else:
                self.change_status("light blue", "light blue",
                                   "Charger Status: Connected")

        # If the charger is NOT plugged in...
        else:

            # If the charger was diconnected while the program is running
            if self.disconnect_per != 0:
                delta = datetime.now() - self.disconnect_time
                self.elapsed_time.configure(
                    text=f"Consumed {self.disconnect_per - self.battery_percentage}% in: {self.convert_time(delta.total_seconds())}")

            # Change the colors according to battery percentage
            if self.battery_percentage > 60:
                self.change_status("green", "red",
                                   "Charger Status: Disconnected")

            elif self.battery_percentage > 30:
                self.change_status("yellow", "red",
                                   "Charger Status: Disconnected")

            else:
                self.change_status("red", "red",
                                   "Charger Status: Disconnected")

        # Update the data every 1 second
        self.after(1000, self.update_data)

    # Function to create the widgets of the UI
    def create_widgets(self):
        # Frame to incase all of the widgets
        main_frame = customtkinter.CTkFrame(
            self, border_width=7, fg_color='black', border_color="#383a3d")
        main_frame.pack()

        # Percentage Label
        self.laptop_percentage = customtkinter.CTkLabel(
            main_frame, text="Battery Level:", font=customtkinter.CTkFont(size=18, weight="bold"), bg_color='black')
        self.laptop_percentage.pack(pady=(12, 0))

        # Percentage Progress bar
        self.percentage_progressbar = customtkinter.CTkProgressBar(
            main_frame, width=290, height=20, bg_color='black')
        self.percentage_progressbar.pack(padx=12)

        # Status of Charger Label
        self.charger_status = customtkinter.CTkLabel(
            main_frame, text="Charger Status:", font=customtkinter.CTkFont(size=15, weight="bold"), bg_color='black')
        self.charger_status.pack()

        # Estimated Time Label
        self.eta_time = customtkinter.CTkLabel(main_frame, text="Time Remaining:", font=customtkinter.CTkFont(
            size=15, weight="bold"), bg_color='black')
        self.eta_time.pack()

        # Elapsed time since charger was diconnected or program started
        self.elapsed_time = customtkinter.CTkLabel(
            main_frame, text="Consumed _ in: _ : _ : _", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.elapsed_time.pack()

        # Close Button
        self.close_button = customtkinter.CTkButton(main_frame, text="Exit Widget", font=customtkinter.CTkFont(
            size=13, weight="bold"), text_color="light yellow", command=self.close, bg_color='black', fg_color="black", hover_color="#383a3d")
        self.close_button.pack(pady=(0, 12))

        # Bind the self window with mouse movement to be able to move it
        self.bind("<B1-Motion>", self.move_window)
        self.bind("<Button-1>", self.get_pos)
