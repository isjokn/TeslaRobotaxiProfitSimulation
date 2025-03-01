import numpy as np

# Constants
YEARS = 3.5  # Model over 3.5 years
MILES_PER_YEAR = 60000  # Miles per year per vehicle
VEHICLE_COST = 30000  # Cost of a robotaxi
VEHICLE_LIFESPAN = 3.5  # Years of operation
ENERGY_COST_PER_MILE = 0.04  # Cost per mile for electricity
MAINTENANCE_COST_PER_MILE = 0.04  # Cost per mile for maintenance
PLATFORM_FEE = 0.50  # Platform fee (revenue split)
SAFETY_DRIVER_COST_PER_HOUR = 0  # Hourly cost for safety driver (set to 0)
FLEET_SIZE = 1  # Number of vehicles in the fleet
FSD_SUBSCRIPTION = 2388  # Annual FSD subscription cost

# Function to calculate revenue per mile
def revenue_per_mile(willingness_to_pay, platform_fee):
    """
    Calculate revenue per mile based on customer's willingness to pay and platform fee.
    
    Args:
        willingness_to_pay (float): Amount customers are willing to pay per mile
        platform_fee (float): Fraction of revenue taken by the platform
    
    Returns:
        float: Revenue per mile after platform fee
    """
    return willingness_to_pay * (1 - platform_fee)

# Monte Carlo simulation function
def monte_carlo_simulation(num_simulations=1000):
    """
    Run a Monte Carlo simulation to estimate robotaxi profitability.
    
    Args:
        num_simulations (int): Number of simulation iterations (default: 1000)
    
    Returns:
        tuple: Mean profit, profit standard deviation, mean manual miles,
               mean autonomous miles, mean revenue per mile, mean cost per mile
    """
    results = []
    manual_miles_results = []
    autonomous_miles_results = []
    revenue_results = []  # List to collect revenue per mile values
    cost_per_mile_results = []  # List to collect average cost per mile per simulation
    
    for _ in range(num_simulations):
        total_profit = 0
        book_value = VEHICLE_COST  # Initial book value
        cumulative_miles = 0
        total_miles = MILES_PER_YEAR * VEHICLE_LIFESPAN  # Total lifespan miles (210,000)
        total_cost_sim = 0  # Accumulate total cost for this simulation
        
        # Residual value is set once per simulation
        residual_value = np.random.uniform(0.05, 0.20) * VEHICLE_COST
        
        # Simulate each full year
        for year in range(int(VEHICLE_LIFESPAN)):  # Years 0, 1, 2
            # Randomize variables for the year
            willingness_to_pay = np.random.normal(2.00, 0.10)
            occupancy_rate = np.random.uniform(0.2, 0.6)
            autonomous_success_rate = np.random.uniform(0.70, 0.99)
            
            # Miles driven this year (fixed for simplicity)
            miles_driven = MILES_PER_YEAR
            cumulative_miles += miles_driven
            
            # Non-linear depreciation (exponential decay based on cumulative miles)
            book_value_end = VEHICLE_COST * (residual_value / VEHICLE_COST) ** (cumulative_miles / total_miles)
            depreciation = book_value - book_value_end
            book_value = book_value_end  # Update book value for next year
            
            # Depreciation cost per mile for this year
            depreciation_per_mile = depreciation / miles_driven
            
            # Total cost per mile (excluding safety driver cost initially)
            cost_per_mile = depreciation_per_mile + ENERGY_COST_PER_MILE + MAINTENANCE_COST_PER_MILE
            
            # Revenue per mile
            revenue = revenue_per_mile(willingness_to_pay, PLATFORM_FEE)
            revenue_results.append(revenue)  # Collect revenue for averaging
            
            # Adjust for autonomous vs. manual miles
            autonomous_miles = miles_driven * autonomous_success_rate
            manual_miles = miles_driven - autonomous_miles
            manual_hours = manual_miles / 20  # Assuming 20 mph average speed
            
            # Safety driver cost per mile
            safety_driver_cost = SAFETY_DRIVER_COST_PER_HOUR * manual_hours / miles_driven
            
            # Adjusted cost including safety driver
            adjusted_cost = cost_per_mile + safety_driver_cost
            total_cost_sim += adjusted_cost * miles_driven  # Add to total cost
            
            # Profit per mile
            profit_per_mile = revenue - adjusted_cost
            
            # Annual profit for this year
            annual_profit = profit_per_mile * miles_driven * occupancy_rate
            total_profit += annual_profit
            
            # Store miles data
            manual_miles_results.append(manual_miles)
            autonomous_miles_results.append(autonomous_miles)
        
        # Handle partial year (0.5 years)
        if VEHICLE_LIFESPAN % 1 != 0:
            fractional_year = VEHICLE_LIFESPAN % 1  # 0.5
            miles_driven = MILES_PER_YEAR * fractional_year
            cumulative_miles += miles_driven
            
            # Randomize variables for partial year
            willingness_to_pay = np.random.normal(2.00, 0.10)
            occupancy_rate = np.random.uniform(0.2, 0.6)
            autonomous_success_rate = np.random.uniform(0.70, 0.99)
            
            # Continue depreciation calculation
            book_value_end = VEHICLE_COST * (residual_value / VEHICLE_COST) ** (cumulative_miles / total_miles)
            depreciation = book_value - book_value_end
            depreciation_per_mile = depreciation / miles_driven
            
            cost_per_mile = depreciation_per_mile + ENERGY_COST_PER_MILE + MAINTENANCE_COST_PER_MILE
            revenue = revenue_per_mile(willingness_to_pay, PLATFORM_FEE)
            revenue_results.append(revenue)  # Collect revenue for partial year
            
            autonomous_miles = miles_driven * autonomous_success_rate
            manual_miles = miles_driven - autonomous_miles
            manual_hours = manual_miles / 20
            safety_driver_cost = SAFETY_DRIVER_COST_PER_HOUR * manual_hours / miles_driven
            adjusted_cost = cost_per_mile + safety_driver_cost
            total_cost_sim += adjusted_cost * miles_driven  # Add to total cost
            
            profit_per_mile = revenue - adjusted_cost
            annual_profit = profit_per_mile * miles_driven * occupancy_rate
            total_profit += annual_profit
            
            manual_miles_results.append(manual_miles)
            autonomous_miles_results.append(autonomous_miles)
        
        # Compute average cost per mile for this simulation
        average_cost_per_mile_sim = total_cost_sim / (MILES_PER_YEAR * VEHICLE_LIFESPAN)
        cost_per_mile_results.append(average_cost_per_mile_sim)
        
        # Average annual profit for this simulation
        average_annual_profit = total_profit / VEHICLE_LIFESPAN
        results.append(average_annual_profit)
    
    # Aggregate results
    mean_profit = np.mean(results)
    std_profit = np.std(results)
    mean_manual_miles = np.mean(manual_miles_results)
    mean_autonomous_miles = np.mean(autonomous_miles_results)
    mean_revenue_per_mile = np.mean(revenue_results)
    mean_cost_per_mile = np.mean(cost_per_mile_results)
    
    return mean_profit, std_profit, mean_manual_miles, mean_autonomous_miles, mean_revenue_per_mile, mean_cost_per_mile

# Run the simulation
mean_profit, std_profit, mean_manual_miles, mean_autonomous_miles, mean_revenue_per_mile, mean_cost_per_mile = monte_carlo_simulation()

# Subtract FSD Subscription Fees
Actual_Profit = mean_profit - FSD_SUBSCRIPTION

# Calculate Total Fleet Profit
Total_Fleet_Profit = Actual_Profit * FLEET_SIZE

# Calculate Average Annual Cost and Revenue
mean_annual_cost = mean_cost_per_mile * MILES_PER_YEAR
mean_annual_revenue = mean_revenue_per_mile * MILES_PER_YEAR

# Print results
print(f"Average Annual Profit per Robotaxi: ${Actual_Profit:,.2f}")
print(f"Average Annual Cost per Robotaxi: ${mean_annual_cost:,.2f}")
print(f"Average Annual Revenue per Robotaxi: ${mean_annual_revenue:,.2f}")
print(f"Standard Deviation of Profit: ${std_profit:,.2f}")
print(f"Total Robotaxis in Fleet: {FLEET_SIZE:.0f}")
print(f"Total Annual Fleet Profit: ${Total_Fleet_Profit:,.2f}")
print(f"Average Manual (Non FSD) Miles Travelled Per Year: {mean_manual_miles:,.2f}")
print(f"Average FSD Miles Travelled Per Year: {mean_autonomous_miles:,.2f}")
print(f"Average Revenue Per Mile: ${mean_revenue_per_mile:,.2f}")
print(f"Average Cost Per Mile: ${mean_cost_per_mile:,.2f}")
