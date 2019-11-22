#!/Users/vibhamasti/anaconda3/bin/python

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time

import simpleaudio as sa

# TODO: make gui pretty
# TODO: comment

class AlarmClock():
    def __init__(self):
        # Initialise audio
        self.wav_obj = sa.WaveObject.from_wave_file('alarm_sound.wav')

        # Read alarms from file
        file = open('alarms.txt', 'r')
        self.alarms = [line.strip() for line in file.readlines()]
        file.close()
        
        # Sort the alarms
        self.alarms.sort()

        # Master
        self.master = Tk()
        self.master.title('Alarm clock')
        self.master.geometry('400x300')


        # Alarm Clock label
        self.label = Label(self.master, text='Alarm Clock', font=('Arial Bold', 25))
        self.label.pack()

        # Left frame
        self.left = Frame(self.master)
        self.left.pack(side=LEFT)

        # Right frame
        self.right = Frame(self.master)
        self.right.pack(side=RIGHT)

        ###### LEFT FRAME ######

        # Button
        self.button = Button(self.left, text='Add alarm', command=self.add_alarm)
        self.button.pack()

        # New alarm labels
        h_label = Label(self.left, text='Hours')
        h_label.pack(side=LEFT)
        m_label = Label(self.left, text='Minutes')
        m_label.pack(side=RIGHT)

        # Hours drop down list
        self.h = IntVar()
        hours = OptionMenu(self.left, self.h, *range(0, 24))
        hours.pack(side=LEFT)

        # Minutes drop down list
        self.m = IntVar()
        minutes = OptionMenu(self.left, self.m, *range(0, 60))
        minutes.pack(side=RIGHT)

        ###### RIGHT FRAME #######
        self.scrollbar = Scrollbar(self.right)
        self.canvas = Canvas(self.right, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.scrollbar.config(command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        # Alarm list frame
        self.alarm_frame = Frame(self.canvas)


        self.canvas.create_window(0,0,window=self.alarm_frame, anchor='nw')

        # List of all alarms
        self.listbox = Listbox(self.alarm_frame)
        self.listbox.pack()
        
        for alarm in self.alarms:
            self.listbox.insert(END, alarm)

        # Attach listbox to scrollbar
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        # Check if alarm should be rung
        self.master.after(1000, self.check_alarm)


    # Check if alarm should be rung
    def check_alarm(self):
        now = time.strftime('%H:%M')
        now_s = int(time.strftime('%S'))

        # Go through all the alarms saved
        for alarm in self.alarms:
            # If an alarm is saved for the current time
            if now == alarm:
                # Message box pop-up with alarm sound
                play_obj = self.wav_obj.play()
                messagebox.showinfo('ALARM', 'ALARM at {}!!!!!!!!!!!!!'.format(now))
                play_obj.stop()

                # Check for alarm in the next minute
                self.master.after((60-now_s)*1000, self.check_alarm)
                return

        self.master.after(1000, self.check_alarm)


    # Add a new alarm
    def add_alarm(self):
        file = open('alarms.txt', 'w')

        # Add a 0 before single-digit times
        time_h = str(self.h.get())
        if len(time_h) == 1:
            time_h = '0' + time_h
        time_m = str(self.m.get())
        if len(time_m) == 1:
            time_m = '0' + time_m

        time_str = time_h+':'+time_m

        if time_str in self.alarms:
            return

        self.alarms.append(time_str)
        self.alarms.sort()
        for alarm in self.alarms:
            file.write(alarm + '\n')

        # Update list of all alarms
        self.listbox.delete(0, END)
        for alarm in self.alarms:
            self.listbox.insert(END, alarm)
        
        file.close()

    # Start the alarm clock loop
    def start(self):
        self.master.mainloop()

    
clk = AlarmClock()
clk.start()