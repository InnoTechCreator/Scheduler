# Copyright 2025 InnoTechCreator
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import DateEntry
import random

class DeploymentSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated Deployment Scheduler")
        self.root.geometry("1000x600")

        # UI Elements
        self.label = tk.Label(root, text="Ship Itinerary Import", font=("Arial", 12, "bold"))
        self.label.pack(pady=10)

        self.brand_label = tk.Label(root, text="Select Brands:")
        self.brand_label.pack()
        self.brand_frame = tk.Frame(root)
        self.brand_frame.pack()
        
        self.brand_vars = {}
        self.brand_ship_lists = {}
        self.all_ships_vars = {}
        self.ships_by_brand = {
            "Carnival Cruise Line": ["Carnival Breeze", "Carnival Vista", "Carnival Horizon", "Carnival Dream"],
            "Princess Cruises": ["Regal Princess", "Royal Princess", "Sky Princess", "Majestic Princess"],
            "Holland America Line": ["MS Rotterdam", "MS Koningsdam", "MS Eurodam", "MS Nieuw Amsterdam"],
            "Costa Cruises": ["Costa Smeralda", "Costa Toscana", "Costa Diadema", "Costa Fascinosa"],
            "Seabourn": ["Seabourn Encore", "Seabourn Ovation", "Seabourn Quest", "Seabourn Sojourn"]
        }
        
        self.brand_selection_frame = tk.Frame(self.brand_frame)
        self.brand_selection_frame.pack()
        
        self.search_label = tk.Label(root, text="Search Ship:")
        self.search_label.pack()
        self.search_entry = tk.Entry(root)
        self.search_entry.pack()
        self.search_entry.bind("<KeyRelease>", self.filter_ships)
        
        for brand in self.ships_by_brand.keys():
            brand_frame = tk.Frame(self.brand_selection_frame)
            brand_frame.pack(side='left', padx=10, anchor='n')
            
            var = tk.IntVar()
            chk = tk.Checkbutton(brand_frame, text=brand, variable=var, command=lambda b=brand: self.toggle_brand_selection(b))
            chk.pack()
            self.brand_vars[brand] = var
            
            all_ships_var = tk.IntVar()
            all_chk = tk.Checkbutton(brand_frame, text="All Ships", variable=all_ships_var, command=lambda b=brand: self.select_all_ships(b))
            all_chk.pack()
            self.all_ships_vars[brand] = all_ships_var
            
            ship_listbox = tk.Listbox(brand_frame, selectmode=tk.MULTIPLE, height=5, exportselection=False)
            ship_listbox.pack()
            self.brand_ship_lists[brand] = ship_listbox
        
        self.date_label = tk.Label(root, text="Select Deployment Start Date:")
        self.date_label.pack()
        self.date_picker = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_picker.pack(pady=5)
        
        self.duration_label = tk.Label(root, text="Enter Deployment Duration (hours):")
        self.duration_label.pack()
        self.duration_entry = tk.Entry(root)
        self.duration_entry.pack(pady=5)
        
        # New Checkbox: Home Ports Only
        self.homeports_only_var = tk.IntVar()
        self.homeports_only_checkbox = tk.Checkbutton(root, text="Home Ports Only", variable=self.homeports_only_var)
        self.homeports_only_checkbox.pack(pady=5)

        self.schedule_button = tk.Button(root, text="Generate Optimized Schedule", command=self.optimize_schedule)
        self.schedule_button.pack(pady=5)

        # Increase the number of rows for a better sample dataset.
        num_rows = 200  
        ship_names = random.choices(sum(self.ships_by_brand.values(), []), k=num_rows)
        ports = random.choices(["Miami", "Nassau", "Cozumel", "Galveston", "New Orleans"], k=num_rows)
        arrival_dates = pd.date_range(start="2025-03-01", periods=num_rows, freq='D')
        departure_dates = pd.date_range(start="2025-03-02", periods=num_rows, freq='D')
        # Deployment Window values are kept as strings but represent hours.
        deployment_window = random.choices(["6", "8", "10", "12"], k=num_rows)
        # Priority is randomly generated in the dataset but will be overridden in the schedule generation.
        priority = random.choices(["High", "Medium", "Low"], k=num_rows)
        # Simulate Home Port data (normally imported from Excel)
        home_ports = [random.choice(["Miami", "Galveston", "New Orleans"]) for _ in range(num_rows)]
        # Randomly mark days as sea days
        sea_day = [random.choice([True, False]) for _ in range(num_rows)]
        # For non-sea days, assign if the casino is open or closed
        casino_status = [random.choice(["Closed", "Open"]) if not sd else "N/A" for sd in sea_day]
        
        self.df = pd.DataFrame({
            "Ship Name": ship_names,
            "Port": ports,
            "Home Port": home_ports,
            "Arrival Date": arrival_dates.strftime('%Y-%m-%d'),
            "Departure Date": departure_dates.strftime('%Y-%m-%d'),
            "Deployment Window": deployment_window,
            "Priority": priority,
            "Sea Day": sea_day,
            "Casino": casino_status
        })
    
    def filter_ships(self, event):
        search_text = self.search_entry.get().lower()
        for brand, ship_listbox in self.brand_ship_lists.items():
            ship_listbox.delete(0, tk.END)
            for ship in self.ships_by_brand[brand]:
                if search_text in ship.lower():
                    ship_listbox.insert(tk.END, ship)
    
    def toggle_brand_selection(self, brand):
        ship_listbox = self.brand_ship_lists[brand]
        ship_listbox.delete(0, tk.END)
        if self.brand_vars[brand].get():
            for ship in self.ships_by_brand[brand]:
                ship_listbox.insert(tk.END, ship)
        else:
            self.all_ships_vars[brand].set(0)
            ship_listbox.delete(0, tk.END)
    
    def select_all_ships(self, brand):
        ship_listbox = self.brand_ship_lists[brand]
        if self.all_ships_vars[brand].get():
            self.brand_vars[brand].set(1)
            ship_listbox.delete(0, tk.END)
            for ship in self.ships_by_brand[brand]:
                ship_listbox.insert(tk.END, ship)
            for i in range(ship_listbox.size()):
                ship_listbox.selection_set(i)
        else:
            self.brand_vars[brand].set(0)
            ship_listbox.delete(0, tk.END)
    
    def get_selected_ships(self):
        """
        Gathers the selected ships from the UI.
        If a brand is checked but no specific ships are selected,
        it assumes all ships under that brand are selected.
        """
        selected_ships = []
        for brand in self.ships_by_brand.keys():
            if self.brand_vars[brand].get() == 1:
                listbox = self.brand_ship_lists[brand]
                selections = listbox.curselection()
                if selections:
                    for idx in selections:
                        ship_name = listbox.get(idx)
                        if ship_name not in selected_ships:
                            selected_ships.append(ship_name)
                else:
                    for ship in self.ships_by_brand[brand]:
                        if ship not in selected_ships:
                            selected_ships.append(ship)
        print("Selected ships:", selected_ships)  # Debug print
        return selected_ships

    def optimize_schedule(self):
        """
        Generates a deployment schedule by:
         - Filtering based on selected ships.
         - Optionally filtering to only home port records.
         - Skipping sea days.
         - Scheduling deployments:
             - At the home port (always scheduled).
             - At other ports only if the casino is closed.
         - Automatically computing priority based on Deployment Window:
             * Window <= 6 hours: High
             * Window <= 8 hours: Medium
             * Otherwise: Low
        """
        selected_ships = self.get_selected_ships()
        if not selected_ships:
            messagebox.showinfo("No Selection", "Please select at least one ship.")
            return

        filtered_df = self.df[self.df["Ship Name"].isin(selected_ships)]
        print("Filtered DataFrame has", len(filtered_df), "records.")  # Debug print
        
        if self.homeports_only_var.get() == 1:
            filtered_df = filtered_df[filtered_df["Port"] == filtered_df["Home Port"]]
            print("After applying Home Ports Only filter, records:", len(filtered_df))  # Debug print

        schedule_list = []
        for idx, row in filtered_df.iterrows():
            if row["Sea Day"]:
                continue

            if row["Port"] == row["Home Port"]:
                deployment_type = "Home Port Deployment"
                scheduled = True
            else:
                if row["Casino"] == "Closed":
                    deployment_type = "Other Port Deployment (Casino Closed)"
                    scheduled = True
                else:
                    deployment_type = "Other Port Deployment (Casino Open - Skipped)"
                    scheduled = False

            if scheduled:
                # Automatically compute priority based on Deployment Window (converted to integer).
                window = int(row["Deployment Window"])
                if window <= 6:
                    computed_priority = "High"
                elif window <= 8:
                    computed_priority = "Medium"
                else:
                    computed_priority = "Low"
                    
                schedule_list.append({
                    "Ship Name": row["Ship Name"],
                    "Deployment Date": row["Arrival Date"],
                    "Port": row["Port"],
                    "Home Port": row["Home Port"],
                    "Deployment Window": row["Deployment Window"],
                    "Priority": computed_priority,
                    "Deployment Type": deployment_type
                })

        if not schedule_list:
            messagebox.showinfo("Info", "No deployments scheduled based on the current criteria.")
            return
        
        schedule_df = pd.DataFrame(schedule_list)
        self.display_schedule(schedule_df)
    
    def display_schedule(self, schedule_df):
        """
        Displays the generated schedule in a new window using a Treeview.
        Allows the Priority column to be edited via a drop-down list on double-click.
        """
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("Generated Deployment Schedule")
        schedule_window.geometry("800x400")
        
        tree = ttk.Treeview(schedule_window)
        tree.pack(fill=tk.BOTH, expand=True)
        
        tree["columns"] = list(schedule_df.columns)
        tree["show"] = "headings"
        
        for col in schedule_df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        
        for _, row in schedule_df.iterrows():
            tree.insert("", tk.END, values=list(row))
        
        # Define a function to allow editing of the Priority cell.
        def on_double_click(event):
            region = tree.identify("region", event.x, event.y)
            if region != "cell":
                return
            
            column = tree.identify_column(event.x)
            columns = tree["columns"]
            try:
                priority_index = columns.index("Priority")
            except ValueError:
                return
            
            col_index = int(column.replace("#", "")) - 1
            if col_index != priority_index:
                return
            
            rowid = tree.identify_row(event.y)
            if not rowid:
                return
            
            current_value = tree.set(rowid, "Priority")
            x, y, width, height = tree.bbox(rowid, column)
            combobox = ttk.Combobox(schedule_window, values=["High", "Medium", "Low"])
            combobox.place(x=x, y=y, width=width, height=height)
            combobox.set(current_value)
            combobox.focus()
            
            def on_select(event):
                new_value = combobox.get()
                tree.set(rowid, "Priority", new_value)
                combobox.destroy()
            
            combobox.bind("<<ComboboxSelected>>", on_select)
            combobox.bind("<FocusOut>", lambda e: combobox.destroy())
        
        tree.bind("<Double-1>", on_double_click)
        
        # Add an Export button.
        export_btn = tk.Button(schedule_window, text="Export to Excel", command=lambda: self.export_schedule(schedule_df))
        export_btn.pack(pady=10)
    
    def export_schedule(self, schedule_df):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", 
            filetypes=[("Excel Files", "*.xlsx")],
            title="Save Deployment Schedule"
        )
        if file_path:
            try:
                schedule_df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Schedule exported successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export schedule: {e}")

# Run the app
if __name__ == "__main__":
    print("Deployment Scheduler is starting...")
    root = tk.Tk()
    app = DeploymentSchedulerApp(root)
    root.mainloop()
