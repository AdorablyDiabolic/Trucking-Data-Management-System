import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "trucking_data.csv"  # Updated file name
    COLUMNS = ["date", "mileage", "load_type", "delivery_details"]  # Updated columns
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        """Initialize the CSV file with the correct structure."""
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            print(f"{cls.CSV_FILE} not found. Creating a new file...")
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
        except pd.errors.EmptyDataError:
            print(f"{cls.CSV_FILE} is empty. Initializing with default columns...")
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, mileage, load_type, delivery_details):
        try:
            df = pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            print(f"{cls.CSV_FILE} not found. Initializing a new file...")
            cls.initialize_csv()
            df = pd.DataFrame(columns=cls.COLUMNS)

        new_entry = pd.DataFrame([{
            "date": date,
            "mileage": mileage,
            "load_type": load_type,
            "delivery_details": delivery_details,
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(cls.CSV_FILE, index=False)
        print("Entry successfully added!")

    @classmethod
    def get_data(cls):
        """Retrieve data from the CSV."""
        try:
            return pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            print(f"Error: {cls.CSV_FILE} not found. Initializing a new file...")
            cls.initialize_csv()
            return pd.DataFrame(columns=cls.COLUMNS)
        except pd.errors.EmptyDataError:
            print("Error: CSV file is empty. Returning empty dataset...")
            return pd.DataFrame(columns=cls.COLUMNS)


def get_date():
    """Prompt the user for the delivery date."""
    while True:
        try:
            date_input = input("Enter the delivery date (DD-MM-YYYY): ")
            datetime.strptime(date_input, "%d-%m-%Y")
            return date_input
        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY.")


def get_mileage():
    """Prompt the user for the mileage covered."""
    while True:
        try:
            mileage = float(input("Enter mileage (in miles): "))
            if mileage >= 0:
                return mileage
            else:
                print("Mileage cannot be negative.")
        except ValueError:
            print("Please enter a valid number.")


def get_load_type():
    """Prompt the user for the load type."""
    load_types = ["Refrigerated", "Dry", "Hazardous", "Other"]
    print("Select load type:")
    for i, load in enumerate(load_types, 1):
        print(f"{i}. {load}")
    while True:
        try:
            choice = int(input("Enter the number corresponding to the load type: "))
            if 1 <= choice <= len(load_types):
                return load_types[choice - 1]
            else:
                print("Invalid selection. Please choose a number from the list.")
        except ValueError:
            print("Please enter a valid number.")


def get_delivery_details():
    """Prompt the user for delivery details."""
    return input("Enter delivery details (destination, notes, etc.): ")


def confirm_entry(date, mileage, load_type, delivery_details):
    """Confirm the trucking data entry with the user."""
    print("\n--- Confirm Your Entry ---")
    print(f"Date: {date}")
    print(f"Mileage: {mileage} miles")
    print(f"Load Type: {load_type}")
    print(f"Delivery Details: {delivery_details}")
    print("--------------------------")
    while True:
        confirmation = input("Is this correct? (y/n): ").lower()
        if confirmation == 'y':
            return True
        elif confirmation == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")


def add_corrected_entry():
    """Collect and confirm data entry, allowing corrections."""
    while True:
        date = get_date()
        mileage = get_mileage()
        load_type = get_load_type()
        delivery_details = get_delivery_details()

        if confirm_entry(date, mileage, load_type, delivery_details):
            return date, mileage, load_type, delivery_details
        else:
            print("Let's re-enter the data.")


def visualize_data():
    """Visualize trucking metrics."""
    df = CSV.get_data()

    if df.empty:
        print("No data available to visualize.")
        return

    print("Filter by load type? (y/n): ", end="")
    filter_load = input().lower() == 'y'
    if filter_load:
        print("Available load types:", df['load_type'].unique())
        load_type = input("Enter load type to filter: ")
        df = df[df['load_type'] == load_type]

    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
    df = df.sort_values("date")
    plt.plot(df["date"], df["mileage"], marker="o")
    plt.title(f"Mileage Over Time ({load_type if filter_load else 'All'})")
    plt.xlabel("Date")
    plt.ylabel("Mileage (miles)")
    plt.grid()
    plt.show()

    # Visualize load type distribution
    load_counts = df["load_type"].value_counts()
    plt.bar(load_counts.index, load_counts.values)
    plt.title("Load Type Distribution")
    plt.xlabel("Load Type")
    plt.ylabel("Number of Deliveries")
    plt.show()


def show_summary():
    """Display summary statistics for trucking data."""
    df = CSV.get_data()

    if df.empty:
        print("No data available to summarize.")
        return

    try:
        total_deliveries = len(df)
        total_mileage = df['mileage'].sum()
        average_mileage = df['mileage'].mean()
        most_frequent_load = df['load_type'].mode()[0]

        print("\n--- Summary Statistics ---")
        print(f"Total Deliveries: {total_deliveries}")
        print(f"Total Mileage: {total_mileage:.2f} miles")
        print(f"Average Mileage per Delivery: {average_mileage:.2f} miles")
        print(f"Most Frequent Load Type: {most_frequent_load}")
        print("--------------------------\n")
    except KeyError as e:
        print(f"Error: Missing column in data: {e}")
        print("Ensure the CSV file contains the following columns: date, mileage, load_type, delivery_details.")


def help_menu():
    """Display the help menu."""
    print("\n--- Help Menu ---")
    print("1. Add Delivery Entry: Record new delivery details.")
    print("2. Visualize Data: View charts for deliveries.")
    print("3. View Summary Statistics: Get key delivery insights.")
    print("4. Help: View this menu.")
    print("5. Exit: Close the program.")
    print("--------------------------")


def main():
    """Main function to run the trucking delivery tracker."""
    CSV.initialize_csv()

    while True:
        print("\n--- Trucking Delivery Tracker ---")
        print("1. Add Delivery Entry")
        print("2. Visualize Data")
        print("3. View Summary Statistics")
        print("4. Help")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            date, mileage, load_type, delivery_details = add_corrected_entry()
            CSV.add_entry(date, mileage, load_type, delivery_details)
        elif choice == "2":
            visualize_data()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            help_menu()
        elif choice == "5":
            print("Exiting the tracker. Safe travels!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
