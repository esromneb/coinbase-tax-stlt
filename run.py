import csv
import sys

PATH='input/Coinbase-2022-CB-GAINLOSSCSV_.csv'
OPATH='output.csv'


from dataclasses import dataclass

@dataclass
class CoinStats:
    amount: float = 0.0
    proceeds: float = 0.0
    st_cost_basis: float = 0.0
    lt_cost_basis: float = 0.0
    st_proceeds: float = 0.0  # short term
    lt_proceeds: float = 0.0  # long term
    st_net: float = 0.0
    lt_net: float = 0.0

    def __str__(self):
        attributes = {
            'Amount': self.amount,
            'Proceeds': self.proceeds,
            'ST Cost Basis': self.st_cost_basis,
            'LT Cost Basis': self.lt_cost_basis,
            'Short Term Proceeds': self.st_proceeds,
            'Long Term Proceeds': self.lt_proceeds,
            'Short Term Net': self.st_net,
            'Long Term Net': self.lt_net,
            'Net': (self.st_net+self.lt_net)
        }
        attribute_str = ""
        for key, value in attributes.items():
            attribute_str += f"{key}={value}, "
        # Remove the trailing comma and space
        attribute_str = attribute_str.rstrip(", ")

        return f"Transaction: {attribute_str}"

# Initialize a dictionary to store the statistics
asset_statistics = {}


def get_names(p):
    with open(p, 'r') as file:
        reader = csv.DictReader(file)
        # Iterate over each row in the CSV file
        ret = []
        for row in reader:
            asset_name = row['Asset name']
            if asset_name not in ret:
                ret.append(asset_name)
    return ret


all_names = get_names(PATH)

# all_names.append('foo')
print(all_names)

# summary = [CoinStats(amount=0, proceeds=0, cost_basis=0, lt_proceeds=0, st_proceeds=0) for x in all_names]

# A dict where key is the asset name
summary = {key: CoinStats() for key in all_names}
# print(summary)
# sys.exit(0)

verbose=False
year = 365


# Open the CSV file
with open(PATH, 'r') as file:
    reader = csv.DictReader(file)

    # print(all_names)
    # print("-------")

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

        # if this fails the code is internally broken
        assert(asset_name in summary)

        # strictly greater than one year
        long_term = holding_period > year
        if long_term:
            summary[asset_name].lt_cost_basis += cost_basis
            summary[asset_name].lt_proceeds += proceeds
            summary[asset_name].lt_net += (proceeds-cost_basis)

        else:
            summary[asset_name].st_cost_basis += cost_basis
            summary[asset_name].st_proceeds += proceeds
            summary[asset_name].st_net += (proceeds-cost_basis)


        if verbose:
            print(f"Transaction Type: {transaction_type}")
            print(f"Asset Name: {asset_name}")
            print()


# # Print the asset statistics
# print("Asset Statistics:")
# for asset, count in asset_statistics.items():
#     print(f"{asset}: {count} occurrences")

total = CoinStats()



total = CoinStats(
    amount=sum(x.amount for x in summary.values()),
    proceeds=sum(x.proceeds for x in summary.values()),
    st_cost_basis=sum(x.st_cost_basis for x in summary.values()),
    lt_cost_basis=sum(x.lt_cost_basis for x in summary.values()),
    st_proceeds=sum(x.st_proceeds for x in summary.values()),
    lt_proceeds=sum(x.lt_proceeds for x in summary.values()),
    st_net=sum(x.st_net for x in summary.values()),
    lt_net=sum(x.lt_net for x in summary.values()),
)

for name, stat in summary.items():
    print(f"{name}------------:")
    print(stat)

with open(OPATH, 'w') as file:
    file.write('Term, Type, '              'Proceeds, '       'Cost basis, Net gain or loss(-)\n')
    file.write(f'Short, Total Short-Term, {total.st_proceeds}, {total.st_cost_basis}, {total.st_net}\n')
    file.write(f'Long, Total Long-Term, {total.lt_proceeds}, {total.lt_cost_basis}, {total.lt_net}\n')

    # for item in items:
    #     file.write(item + '\n')

# I proved that I can sum correctly
# for each entry, track the short term cost basis and proceeds
# proceeds are how much I sold for, not profits

# So I want cost and sell price

# coinbase just reported the net gain or loss
