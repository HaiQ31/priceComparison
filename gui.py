import tkinter as tk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import numpy as np

matplotlib.use('TkAgg')


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tarifvergleich')

        # set frames for chart and input
        self.frm_chart = tk.Frame(master=self)
        self.frm_chart.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frm_inputs = tk.Frame(master=self)
        self.frm_inputs.pack(side=tk.LEFT, anchor='nw', expand=False)
        # button frame
        self.frm_draw_button = tk.Frame(master=self.frm_inputs)
        self.frm_draw_button.pack(side=tk.TOP, pady=10)
        # names frame
        self.frm_input_names = tk.Frame(master=self.frm_inputs)
        self.frm_input_names.pack(side=tk.TOP, anchor="nw", expand=False, padx=10, pady=10)

        # prepare data input
        # name
        lbl_name = tk.Label(text='Name', master=self.frm_input_names)
        lbl_name.pack(side=tk.LEFT, padx=90)
        # base price
        lbl_base_price = tk.Label(text='Grundpreis', master=self.frm_input_names)
        lbl_base_price.pack(side=tk.LEFT, padx=60)
        # working price
        lbl_working_price = tk.Label(text='Arbeitspreis', master=self.frm_input_names)
        lbl_working_price.pack(side=tk.LEFT, padx=0)

        # loop over rows
        self.rows = {}
        number_of_rows = 3
        for i in range(number_of_rows):
            self.add_row()

        # create a figure
        figure = Figure()
        self.ax = figure.add_subplot(111)

        # create List for lines
        self.lines = [] #löschen?

        # create FigureCanvasTkAgg object
        self.figure_canvas = FigureCanvasTkAgg(figure, master=self.frm_chart)

        # create the toolbar
        NavigationToolbar2Tk(self.figure_canvas, self.frm_chart)

        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # draw button
        btn_draw = tk.Button(text="draw", master=self.frm_draw_button,
                             command=lambda: self.draw(self.rows))
        btn_draw.pack()

        # add row button
        btn_add_row = tk.Button(text="add row", master=self.frm_inputs, command=lambda: self.add_row())
        btn_add_row.pack(side=tk.BOTTOM, pady=5)

    def add_row(self):
        # get idx of last item
        if not self.rows:
            i = 0
        else:
            i = list(self.rows.keys())[-1]
            i = i+1

        # row frame
        frm_row = tk.Frame(master=self.frm_inputs)
        frm_row.pack(side=tk.TOP, pady=5)

        frm_row_name = tk.Frame(master=frm_row)
        frm_row_name.pack(side=tk.LEFT, padx=0)
        frm_row_base_price = tk.Frame(master=frm_row)
        frm_row_base_price.pack(side=tk.LEFT, padx=20)
        frm_row_working_price = tk.Frame(master=frm_row)
        frm_row_working_price.pack(side=tk.LEFT, padx=0)

        lbl_row_number = tk.Label(text=i + 1, master=frm_row_name)
        lbl_row_number.pack(side=tk.LEFT, padx=10)
        ent_name = tk.Entry(master=frm_row_name)
        ent_name.pack(side=tk.LEFT)
        ent_base_price = tk.Entry(master=frm_row_base_price, width=6)
        ent_base_price.pack(side=tk.LEFT)
        lbl_base_price_disc = tk.Label(text="€/Monat", master=frm_row_base_price)
        lbl_base_price_disc.pack(side=tk.LEFT)
        ent_working_price = tk.Entry(master=frm_row_working_price, width=6)
        ent_working_price.pack(side=tk.LEFT)
        lbl_working_price_disc = tk.Label(text="€/kWh", master=frm_row_working_price)
        lbl_working_price_disc.pack(side=tk.LEFT)

        # store in dict
        row = {}
        row["no"] = lbl_row_number
        row["name"] = ent_name
        row["base_price"] = ent_base_price
        row["working_price"] = ent_working_price
        self.rows[i] = row

    def make_line(self, ax, base_price, working_price, name, lower=1800, upper=3200, step=10):
        steps = np.arange(lower, upper, step)
        values = working_price * steps + base_price * 12
        line = ax.plot(steps, values,
                       label="{name}; {working_price:.2f}€/kWh, {base_price:.2f}€/mo".format(
                           name=name, working_price=working_price, base_price=base_price))
        self.lines.append(line) #löschen?

    def draw(self, rows):
        # delete old chart
        self.ax.clear()

        # loop over entry rows
        for k, v in rows.items():
            if v["name"].get() == '':
                continue
            name = v["name"].get()
            base_price = float(v["base_price"].get())
            working_price = float(v["working_price"].get())
            self.make_line(self.ax, base_price, working_price, name, lower=1800, upper=3200, step=10)

        # color x-spine like cheapest price
        color = []  # hier sind die verwendeten Farben gespeichert.
        label = []
        for line in self.ax.lines:
            color.append(line.get_color())
            label.append(line.get_label())

        self.ax.legend()
        self.figure_canvas.draw()


def test_placeholder():
    pass


if __name__ == '__main__':
    app = App()
    app.mainloop()
