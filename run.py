import csv

PATH='input/Coinbase-2022-CB-GAINLOSSCSV_.csv'



# Open the CSV file
with open(PATH, 'r') as file:
    reader = csv.DictReader(file)

    # Initialize a dictionary to store the statistics
    asset_statistics = {}

    # Iterate over each row in the CSV file
    for row in reader:
        # Access the columns based on their names
        transaction_type = row['Transaction Type']
        transaction_id = row['Transaction ID']
        tax_lot_id = row['Tax lot ID']
        asset_name = row['Asset name']
        amount = float(row['Amount'])
        date_acquired = row['Date Acquired']
        cost_basis = float(row['Cost basis (USD)'])
        date_of_disposition = row['Date of Disposition']
        proceeds = float(row['Proceeds (USD)'])
        gains_losses = float(row['Gains (Losses) (USD)'])
        holding_period = int(row['Holding period (Days)'])
        data_source = row['Data source']

        # Update the asset statistics
        if asset_name in asset_statistics:
            asset_statistics[asset_name] += 1
        else:
            asset_statistics[asset_name] = 1

        # Do something with the data
        # Example: print the transaction type and asset name
        print(f"Transaction Type: {transaction_type}")
        print(f"Asset Name: {asset_name}")
        print()

    # Print the asset statistics
    print("Asset Statistics:")
    for asset, count in asset_statistics.items():
        print(f"{asset}: {count} occurrences")
