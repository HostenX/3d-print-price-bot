import json
import math

#---Function to calculate the cost per hour of the printer---#
def calculate_cost_per_hour(config):

    #declare printer variable out of JSON File
    p=config["printer"]

    #Calculate the cost per hour of the printer based on its estimated life and duty cycle
    lifetime_hours = p["estimated_life_years"] * 365 * 24 * p["duty_cycle_percent"] / 100

    #calculate the depriciation cost per hour of the printer based on its cost and estimated lifetime
    depricing_per_hour = p["cost_cop"]/lifetime_hours

    #calculate the cost of maintanance per hour of the printer based on its maintenance cost and estimated lifetime
    maintanance_per_hour = (p["annual_maintenance_cop"]) * p["estimated_life_years"] / lifetime_hours

    #calculate electrical use per hour
    electricity_per_hour = (p["power_consumtion_w"]/1000) * p['electricity_cost_cop_kwh']

    base_hour_cost = depricing_per_hour + maintanance_per_hour + electricity_per_hour

    total_cost_per_hour = base_hour_cost * p['buffer_factor']

    return round(total_cost_per_hour, 2)

#---Calculate Material Cost (FDM)---#
def calculate_material_cost_per_hour(config, object_weight_gr):

    m=config["material"]

    cost_per_gram = m["spool_cost_cop"] / m["default_spool_weight_gr"]

    base_material_cost = object_weight_gr * cost_per_gram * m["efficiency_factor"]

    return round(base_material_cost, 2)

#---Round T0 Nearest hundredth (COP)---#
def round_to_nearest_hundredth(value): 
    return math.ceil(value / 100) * 100

#---Main Program---#
#-----OpenJSON Config File-----#
with open('var.json', 'r', encoding="utf-8") as file:

    config = json.load(file)
#-----Save Variables from JSON File-----#
printer_cost_per_hour = calculate_cost_per_hour(config)

simulated_object_weight_gr = 330   # Example weight in grams
simulated_time_spent_hr = 26.4         # Example time spent in hours
simulated_prep_time_min = 0        # Example preparation time in minutes

#------Calculate Printed Object Cost------#
material_spent = calculate_material_cost_per_hour(config, simulated_object_weight_gr)
machine_spent = printer_cost_per_hour * simulated_time_spent_hr

#------Calculate Labor Cost------#
labor_rate_per_hour = config["labor"]["rate_cop_hour"]
labor_spent = (simulated_prep_time_min / 60) * labor_rate_per_hour

total_production_cost = machine_spent + material_spent + labor_spent

#------Calculate Profit Margin------#
margin_percent = 1 - (config["Business"]["profit_margin_percent"] / 100)

raw_price = total_production_cost / margin_percent

#------Round Price to Nearest Hundredth------#
final_price = round_to_nearest_hundredth(raw_price)

#-----Print Results-----#

print("==================================================")
print(f"COTIZACIÓN PARA: {config['printer']['name']}")
print("==================================================")
print(f"Costo Máquina ({simulated_time_spent_hr}h):      ${machine_spent:.2f} COP")
print(f"Costo Material ({simulated_object_weight_gr}g):  ${material_spent:.2f} COP")
print(f"Mano de Obra ({simulated_prep_time_min} min):   ${labor_spent:.2f} COP")
print(f"Costo Total Fabricación: ${total_production_cost:.2f} COP")
print("--------------------------------------------------")
print(f"Precio Bruto con Margen: ${raw_price:.2f} COP")
print(f"PRECIO SUGERIDO AL CLIENTE: ${final_price:.2f} COP")
print("==================================================")
