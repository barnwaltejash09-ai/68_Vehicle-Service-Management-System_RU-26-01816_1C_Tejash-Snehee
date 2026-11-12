import os

class ServiceRecord:
    PRICE_LIST = {
        "Oil Change": 1500,
        "Wheel Alignment": 800,
        "Full Service": 4500,
        "Brake Repair": 2200
    }

    def __init__(self, reg_no, owner, vehicle_type, service_type, status="Pending"):
        self.reg_no = reg_no
        self.owner = owner
        self.vehicle_type = vehicle_type
        self.service_type = service_type
        self.status = status
        self.cost = self.calculate_cost()

    def calculate_cost(self):
        base_price = self.PRICE_LIST.get(self.service_type, 0)
        return base_price * 1.18

    def display(self):
        return f"{self.reg_no} | {self.service_type} | Cost incl. 18% GST: Rs. {self.cost:.2f} | Status: {self.status}"

    def to_file_string(self):
        return f"{self.reg_no},{self.owner},{self.vehicle_type},{self.service_type},{self.status},{self.cost}\n"


class ServiceManager:
    def __init__(self, filename="services.txt"):
        self.filename = filename
        self.records = {}
        self.load_from_file()

    def load_from_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 6:
                        reg_no, owner, vehicle_type, service_type, status, cost = parts
                        self.records[reg_no] = ServiceRecord(reg_no, owner, vehicle_type, service_type, status)

    def save_to_file(self):
        with open(self.filename, "w") as file:
            for record in self.records.values():
                file.write(record.to_file_string())

    def add_record(self, reg_no, owner, vehicle_type, service_type):
        if service_type not in ServiceRecord.PRICE_LIST:
            print(f"Invalid service type. Choose from: {', '.join(ServiceRecord.PRICE_LIST.keys())}.")
            return
        
        new_record = ServiceRecord(reg_no, owner, vehicle_type, service_type)
        self.records[reg_no] = new_record
        self.save_to_file()
        print(f"Record added. {new_record.display()}")

    def view_records(self):
        if not self.records:
            print("No service records found.")
            return
        print("\n--- All Service Records ---")
        for record in self.records.values():
            print(record.display())
        print("-" * 30)

    def update_status(self, reg_no, new_status):
        if reg_no in self.records:
            old_status = self.records[reg_no].status
            self.records[reg_no].status = new_status
            self.save_to_file()
            print(f"Status updated: {old_status} -> {new_status}")
        else:
            print(f"No record found for {reg_no}.")

    def delete_record(self, reg_no):
        if reg_no in self.records:
            del self.records[reg_no]
            self.save_to_file()
            print(f"Record for {reg_no} deleted.")
        else:
            print(f"No record found for {reg_no}.")


def main():
    manager = ServiceManager()

    while True:
        print("\nMenu:")
        print("1. Add record")
        print("2. View records")
        print("3. Update status")
        print("4. Delete record")
        print("5. Exit")
        
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            reg_no = input("Reg no: ").strip()
            owner = input("Owner: ").strip()
            vehicle = input("Vehicle: ").strip()
            service = input("Service: ").strip()
            manager.add_record(reg_no, owner, vehicle, service)

        elif choice == '2':
            manager.view_records()

        elif choice == '3':
            reg_no = input("Reg no: ").strip()
            new_status = input("New status: ").strip()
            manager.update_status(reg_no, new_status)

        elif choice == '4':
            reg_no = input("Reg no: ").strip()
            manager.delete_record(reg_no)

        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
