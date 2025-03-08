import tkinter as tk
from tkinter import messagebox
import numpy as np
import webbrowser  # Added for contact link functionality

# Function to calculate revenue per mile (example helper function)
def revenue_per_mile(willingness_to_pay, platform_fee):
    return willingness_to_pay * (1 - platform_fee)

# Monte Carlo simulation function (unchanged)
def monte_carlo_simulation(num_simulations, vehicle_cost, vehicle_lifespan, miles_per_year, energy_cost_per_mile,
                           maintenance_cost_per_mile, cleaning_cost_per_year, platform_fee, fsd_subscription, fleet_size):
    results = []
    manual_miles_total = []
    autonomous_miles_total = []
    revenue_results = []
    cost_per_mile_results = []
    occupancy_rate_results = []
    
    for _ in range(num_simulations):
        total_profit = 0
        book_value = vehicle_cost
        cumulative_miles = 0
        total_miles = miles_per_year * vehicle_lifespan
        total_cost_sim = 0
        total_revenue_sim = 0
        total_manual_miles = 0
        total_autonomous_miles = 0
        residual_value = np.random.uniform(0.05, 0.20) * vehicle_cost
        
        for year in range(int(vehicle_lifespan)):
            willingness_to_pay = np.random.normal(2.00, 0.10)
            occupancy_rate = np.random.uniform(0.2, 0.6)
            autonomous_success_rate = np.random.uniform(0.70, 0.99)
            miles_driven = miles_per_year
            cumulative_miles += miles_driven
            
            book_value_end = vehicle_cost * (residual_value / vehicle_cost) ** (cumulative_miles / total_miles)
            depreciation = book_value - book_value_end
            book_value = book_value_end
            depreciation_per_mile = depreciation / miles_driven
            cost_per_mile = depreciation_per_mile + energy_cost_per_mile + maintenance_cost_per_mile + (cleaning_cost_per_year / miles_per_year)
            
            revenue_per_mile_full = revenue_per_mile(willingness_to_pay, platform_fee)
            revenue = revenue_per_mile_full * occupancy_rate
            revenue_results.append(revenue)
            total_revenue_sim += revenue * miles_driven
            occupancy_rate_results.append(occupancy_rate)
            
            profit_per_mile = revenue - cost_per_mile
            total_cost_sim += cost_per_mile * miles_driven
            
            annual_profit = profit_per_mile * miles_driven
            total_profit += annual_profit
            
            manual_miles = miles_driven - (miles_driven * autonomous_success_rate)
            autonomous_miles = miles_driven * autonomous_success_rate
            total_manual_miles += manual_miles
            total_autonomous_miles += autonomous_miles
        
        # Handle fractional years if lifespan is not an integer
        if vehicle_lifespan % 1 != 0:
            fractional_year = vehicle_lifespan % 1
            miles_driven = miles_per_year * fractional_year
            cumulative_miles += miles_driven
            
            willingness_to_pay = np.random.normal(2.00, 0.10)
            occupancy_rate = np.random.uniform(0.2, 0.6)
            autonomous_success_rate = np.random.uniform(0.70, 0.99)
            
            book_value_end = vehicle_cost * (residual_value / vehicle_cost) ** (cumulative_miles / total_miles)
            depreciation = book_value - book_value_end
            depreciation_per_mile = depreciation / miles_driven
            cost_per_mile = depreciation_per_mile + energy_cost_per_mile + maintenance_cost_per_mile + (cleaning_cost_per_year / miles_per_year)
            
            revenue_per_mile_full = revenue_per_mile(willingness_to_pay, platform_fee)
            revenue = revenue_per_mile_full * occupancy_rate
            revenue_results.append(revenue)
            total_revenue_sim += revenue * miles_driven
            occupancy_rate_results.append(occupancy_rate)
            
            profit_per_mile = revenue - cost_per_mile
            total_cost_sim += cost_per_mile * miles_driven
            
            annual_profit = profit_per_mile * miles_driven
            total_profit += annual_profit
            
            manual_miles = miles_driven - (miles_driven * autonomous_success_rate)
            autonomous_miles = miles_driven * autonomous_success_rate
            total_manual_miles += manual_miles
            total_autonomous_miles += autonomous_miles
        
        average_cost_per_mile_sim = total_cost_sim / (miles_per_year * vehicle_lifespan)
        cost_per_mile_results.append(average_cost_per_mile_sim)
        
        average_annual_profit = total_profit / vehicle_lifespan
        results.append(average_annual_profit)
        
        manual_miles_total.append(total_manual_miles / vehicle_lifespan)
        autonomous_miles_total.append(total_autonomous_miles / vehicle_lifespan)
    
    mean_profit = np.mean(results)
    std_profit = np.std(results)
    mean_manual_miles = np.mean(manual_miles_total)
    mean_autonomous_miles = np.mean(autonomous_miles_total)
    mean_revenue_per_mile = np.mean(revenue_results)
    mean_cost_per_mile = np.mean(cost_per_mile_results)
    mean_occupancy_rate = np.mean(occupancy_rate_results)
    mean_cleaning_cost_per_day = cleaning_cost_per_year / 365
    
    # Subtract FSD subscription fees
    actual_profit = mean_profit - fsd_subscription
    
    # Calculate total fleet profit
    total_fleet_profit = actual_profit * fleet_size
    
    # Calculate average annual cost and revenue
    mean_annual_cost = mean_cost_per_mile * miles_per_year
    mean_annual_revenue = mean_revenue_per_mile * miles_per_year
    
    return (mean_profit, std_profit, mean_manual_miles, mean_autonomous_miles, mean_revenue_per_mile, mean_cost_per_mile,
            mean_occupancy_rate, mean_cleaning_cost_per_day, actual_profit, total_fleet_profit, mean_annual_cost, mean_annual_revenue)

# Function to handle GUI form submission (unchanged)
def submit_form():
    try:
        # Retrieve and convert inputs from GUI
        vehicle_cost = float(vehicle_cost_entry.get())
        vehicle_lifespan = float(vehicle_lifespan_entry.get())
        miles_per_year = float(miles_per_year_entry.get())
        energy_cost_per_mile = float(energy_cost_entry.get())
        maintenance_cost_per_mile = float(maintenance_cost_entry.get())
        cleaning_cost_per_year = float(cleaning_cost_entry.get())
        platform_fee = float(platform_fee_entry.get())
        fsd_subscription = float(fsd_subscription_entry.get())
        fleet_size = int(fleet_size_entry.get())
        num_simulations = int(num_simulations_entry.get())
        
        # Basic input validation
        if vehicle_cost <= 0:
            raise ValueError("Vehicle cost must be positive.")
        if vehicle_lifespan <= 0:
            raise ValueError("Vehicle lifespan must be positive.")
        if miles_per_year <= 0:
            raise ValueError("Miles per year must be positive.")
        if num_simulations <= 0:
            raise ValueError("Number of simulations must be positive.")
        
        # Run the simulation with GUI inputs
        (mean_profit, std_profit, mean_manual_miles, mean_autonomous_miles, mean_revenue_per_mile, mean_cost_per_mile,
         mean_occupancy_rate, mean_cleaning_cost_per_day, actual_profit, total_fleet_profit, mean_annual_cost, mean_annual_revenue) = monte_carlo_simulation(
            num_simulations, vehicle_cost, vehicle_lifespan, miles_per_year, energy_cost_per_mile, maintenance_cost_per_mile,
            cleaning_cost_per_year, platform_fee, fsd_subscription, fleet_size
        )
        
        # Format the results for display
        result_string = "===== Robotaxi Profitability Simulation Results =====\n\n"
        result_string += "--- At a Glance ---\n"
        result_string += f"With {miles_per_year:,} miles/year and {mean_occupancy_rate:.2%} occupancy,\n"
        result_string += f"your robotaxi nets ${actual_profit:,.2f} annually after costs.\n\n"
        result_string += "--- Revenue ---\n"
        result_string += f"Average Annual Revenue per Robotaxi:      ${mean_annual_revenue:,.2f}\n"
        result_string += f"Average Revenue Per Mile:                      ${mean_revenue_per_mile:,.2f}\n"
        result_string += f"Average Occupancy Rate:                       {mean_occupancy_rate:.2%}\n\n"
        result_string += "--- Costs ---\n"
        result_string += f"Average Annual Cost per Robotaxi:         ${mean_annual_cost:,.2f}\n"
        result_string += f"Average Cost Per Mile:                         ${mean_cost_per_mile:,.2f}\n"
        result_string += f"Average Cleaning Cost per Day:                ${mean_cleaning_cost_per_day:,.2f}\n"
        result_string += f"FSD Subscription Cost per Year:            ${fsd_subscription:,.2f}\n\n"
        result_string += "--- Profit ---\n"
        result_string += f"Average Annual Profit per Robotaxi:       ${actual_profit:,.2f}\n"
        result_string += f"Standard Deviation of Profit:              ${std_profit:,.2f}\n\n"
        result_string += "--- Fleet Overview ---\n"
        result_string += f"Total Robotaxis in Fleet:                          {fleet_size:.0f}\n"
        result_string += f"Total Annual Fleet Profit:                ${total_fleet_profit:,.2f}\n"
        result_string += f"Average Manual Miles/Year:                 {mean_manual_miles:,.2f}\n"
        result_string += f"Average Autonomous Miles/Year:          {mean_autonomous_miles:,.2f}\n"
        result_string += "=================================================="
        
        # Clear previous results and display new ones
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result_string)
    
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Create the Tkinter GUI window
root = tk.Tk()
root.title("Robotaxi Profitability Simulation")

# Add logo at the top
try:
    logo = tk.PhotoImage(file="/Users/johnknapp/Documents/GitHub/TeslaRobotaxiProfitSimulation/Shrub.jpg")  # Replace with your logo file path
    logo_label = tk.Label(root, image=logo)
    logo_label.image = logo  # Keep a reference to avoid garbage collection
    logo_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
except tk.TclError:
    print("Logo image not found. Please check the file path.")

# Add input fields with labels and default values (rows shifted by +1)
tk.Label(root, text="Vehicle Cost ($):").grid(row=1, column=0, padx=5, pady=5)
vehicle_cost_entry = tk.Entry(root)
vehicle_cost_entry.grid(row=1, column=1, padx=5, pady=5)
vehicle_cost_entry.insert(0, "30000")

tk.Label(root, text="Vehicle Lifespan (years):").grid(row=2, column=0, padx=5, pady=5)
vehicle_lifespan_entry = tk.Entry(root)
vehicle_lifespan_entry.grid(row=2, column=1, padx=5, pady=5)
vehicle_lifespan_entry.insert(0, "3.5")

tk.Label(root, text="Miles per Year:").grid(row=3, column=0, padx=5, pady=5)
miles_per_year_entry = tk.Entry(root)
miles_per_year_entry.grid(row=3, column=1, padx=5, pady=5)
miles_per_year_entry.insert(0, "90000")

tk.Label(root, text="Energy Cost per Mile ($):").grid(row=4, column=0, padx=5, pady=5)
energy_cost_entry = tk.Entry(root)
energy_cost_entry.grid(row=4, column=1, padx=5, pady=5)
energy_cost_entry.insert(0, "0.04")

tk.Label(root, text="Maintenance Cost per Mile ($):").grid(row=5, column=0, padx=5, pady=5)
maintenance_cost_entry = tk.Entry(root)
maintenance_cost_entry.grid(row=5, column=1, padx=5, pady=5)
maintenance_cost_entry.insert(0, "0.04")

tk.Label(root, text="Cleaning Cost per Year ($):").grid(row=6, column=0, padx=5, pady=5)
cleaning_cost_entry = tk.Entry(root)
cleaning_cost_entry.grid(row=6, column=1, padx=5, pady=5)
cleaning_cost_entry.insert(0, "5475")

tk.Label(root, text="Platform Fee (decimal):").grid(row=7, column=0, padx=5, pady=5)
platform_fee_entry = tk.Entry(root)
platform_fee_entry.grid(row=7, column=1, padx=5, pady=5)
platform_fee_entry.insert(0, "0.50")

tk.Label(root, text="FSD Subscription per Year ($):").grid(row=8, column=0, padx=5, pady=5)
fsd_subscription_entry = tk.Entry(root)
fsd_subscription_entry.grid(row=8, column=1, padx=5, pady=5)
fsd_subscription_entry.insert(0, "2388")

tk.Label(root, text="Fleet Size:").grid(row=9, column=0, padx=5, pady=5)
fleet_size_entry = tk.Entry(root)
fleet_size_entry.grid(row=9, column=1, padx=5, pady=5)
fleet_size_entry.insert(0, "1")

tk.Label(root, text="Number of Simulations:").grid(row=10, column=0, padx=5, pady=5)
num_simulations_entry = tk.Entry(root)
num_simulations_entry.grid(row=10, column=1, padx=5, pady=5)
num_simulations_entry.insert(0, "1000")

# Add a submit button to run the simulation
submit_button = tk.Button(root, text="Run Simulation", command=submit_form)
submit_button.grid(row=11, column=0, columnspan=2, pady=10)

# Add a text area to display results
result_text = tk.Text(root, height=20, width=80)
result_text.grid(row=12, column=0, columnspan=2, padx=5, pady=5)

# Add contact link at the bottom
contact_label = tk.Label(root, text="Contact: @reenigneerit on X", fg="blue", cursor="hand2")
contact_label.grid(row=13, column=0, columnspan=2, pady=5)
contact_label.bind("<Button-1>", lambda e: webbrowser.open("https://x.com/reenigneerit"))
contact_label.config(font=("TkDefaultFont", 10, "underline"))

# Start the Tkinter event loop
root.mainloop()
