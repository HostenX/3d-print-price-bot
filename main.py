from MakerWorldScrapper import obtain_data
import json
from CalcPrice import calculate_final_price

with open('var.json', 'r', encoding="utf-8") as file:

        config = json.load(file)


url = "https://makerworld.com/en/models/3055273-extendable-star-fidget-toy?from=search#profileId-3437464"

weight, time_sec, title, time_str = obtain_data(url)

print("=" * 45)
print(f"Model: {title}")
print(f"Estimated Time: {time_str} ({time_sec}s)")
print(f"Total Weight: {weight} g")
print("-" * 45)
time_hr = time_sec / 3600  # Convert seconds to hours

final_price = calculate_final_price(config, weight, time_hr, prep_time_min=0)

print(f"Final Price: ${final_price:.2f} COP")