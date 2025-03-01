import numpy as np

# Constants
YEARS = 3.5  # Model over 5 years
MILES_PER_YEAR = 60000  # Miles per year per vehicle default is 100k
# ESTIMATING 210,00 Total miles over life of vehicle
VEHICLE_COST = 30000  # Cost of a robotaxi default is 30k
VEHICLE_LIFESPAN = 3.5  # Years of operation default is 5
ENERGY_COST_PER_MILE = 0.04  # default is $0.03 per mile for electricity
MAINTENANCE_COST_PER_MILE = 0.04  # default is $0.04 per mile for maintenance
PLATFORM_FEE = 0.50  # default is 25% platform fee (revenue split)
SAFETY_DRIVER_COST_PER_HOUR = 0  # Hourly cost for safety driver phase-out default is 15
FLEET_SIZE = 1  # Number of vehicles in your robotaxi fleet default is 1
FSD_SUBSCRIPTION = 2388

# TODOMARKET_PENETRATION = 0.25  # % ride-hailing market penetration to start- Austin, TX, TAM 240M miles/year
# Small Fleet (1-10 vehicles) 10 robotaxis at 60k miles 0.25% of 240M (TAM)
# If it were to grow to 10% (24M miles) you would need 400 vehicles
# Pay attention to number of robotaxis deployed per market as this number could
# directly impact TAM for even a small to medium fleet if oversaturated


# TODO: Add insurance_cost_per_mile once data available (est. $0.17-$0.42/mile)

# Function to calculate cost per mile for robotaxi operations
def cost_per_mile(vehicle_cost, miles_per_year, vehicle_lifespan, energy_cost, maintenance_cost, residual_value):
    # Depreciation cost now considers residual value
    depreciation_cost = (vehicle_cost - residual_value) / (miles_per_year * vehicle_lifespan)
    total_cost_per_mile = depreciation_cost + energy_cost + maintenance_cost
    return total_cost_per_mile

# Function to estimate revenue based on willingness to pay
def revenue_per_mile(willingness_to_pay, platform_fee):
    return willingness_to_pay * (1 - platform_fee)

# Simulate different scenarios using Monte Carlo default num_simulations is 1000
def monte_carlo_simulation(num_simulations=1000):
    results = []
    manual_miles_results = []
    autonomous_miles_results = []
    
    for _ in range(num_simulations):
        # Simulating variability in key metrics
        willingness_to_pay = np.random.normal(2.00, 0.10)  # Assume $0.50 per mile on average with some variability default 10%
        occupancy_rate = np.random.uniform(0.2, 0.6)  # Varying occupancy rate between 20% and 60%
        autonomous_success_rate = np.random.uniform(0.70, 0.99)  # Varying success rate from 70% to 99%
        
        # Simulate residual value that will be left at the end of the 5 years based on a percentage of initial cost, varying from 5% to 20%
        residual_value = np.random.uniform(0.05, 0.20) * VEHICLE_COST
        
        # Calculate costs and revenues
        cost = cost_per_mile(VEHICLE_COST, MILES_PER_YEAR, VEHICLE_LIFESPAN, ENERGY_COST_PER_MILE, MAINTENANCE_COST_PER_MILE, residual_value)
        revenue = revenue_per_mile(willingness_to_pay, PLATFORM_FEE)
        
        # Adjust cost for autonomous vs. manual driving
        autonomous_miles = MILES_PER_YEAR * autonomous_success_rate
        manual_miles = MILES_PER_YEAR - autonomous_miles
        
        # Convert manual miles to hours assuming a speed of 20 mph for simplicity
        manual_hours = manual_miles / 20  # Assuming 20 mph average speed
        
        # Cost per mile includes safety driver cost when not autonomous
        adjusted_cost = cost + (SAFETY_DRIVER_COST_PER_HOUR * manual_hours / MILES_PER_YEAR)

        # Calculate the Profit Per Mile -NOTE the initial cost of the vehicle is not considered up front but it is considered over the life of the vehicle in the calculations and is already taken out of the profit.
        profit_per_mile = revenue - adjusted_cost
        annual_profit = profit_per_mile * MILES_PER_YEAR * occupancy_rate
        
        # Store results for each simulation
        results.append(annual_profit)
        manual_miles_results.append(manual_miles)
        autonomous_miles_results.append(autonomous_miles)
    
    # Calculate the mean and standard deviation after all simulations
    mean_profit = np.mean(results)
    std_profit = np.std(results)
    mean_manual_miles = np.mean(manual_miles_results)
    mean_autonomous_miles = np.mean(autonomous_miles_results)
    
    return mean_profit, std_profit, mean_manual_miles, mean_autonomous_miles

# Run the simulation
mean_profit, std_profit, mean_manual_miles, mean_autonomous_miles = monte_carlo_simulation()

# Subtract FSD Subscription Fees
Actual_Profit = mean_profit - FSD_SUBSCRIPTION

# Calculate Total_Fleet_Profit using the mean_profit from the simulation * the FLEET_SIZE
Total_Fleet_Profit = Actual_Profit * FLEET_SIZE

print(f"Average Annual Profit per Robotaxi: ${Actual_Profit:,.2f}")
print(f"Standard Deviation of Profit: ${std_profit:,.2f}")
print(f"Total Robotaxis in Fleet: {FLEET_SIZE:.0f}")
print(f"Total Annual Fleet Profit: ${Total_Fleet_Profit:,.2f}")
print(f"Average Manual (Non FSD) Miles Travelled Per Year: {mean_manual_miles:,.2f}")
print(f"Average FSD Miles Travelled Per Year: {mean_autonomous_miles:,.2f}")
