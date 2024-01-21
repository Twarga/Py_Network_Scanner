import tkinter as tk
from tkinter import ttk
import nmap

class NetworkScannerApp:
    def __init__(self, master):
        self.master = master
        master.title("Network Scanner")

        self.create_widgets()

    def create_widgets(self):
        self.label_target = ttk.Label(self.master, text="Target IP:")
        self.entry_target = ttk.Entry(self.master)
        self.label_ports = ttk.Label(self.master, text="Ports to scan:")
        self.entry_ports = ttk.Entry(self.master)
        self.button_scan = ttk.Button(self.master, text="Scan", command=self.scan)
        self.result_text = tk.Text(self.master, height=20, width=60, state=tk.DISABLED)

        self.label_target.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_target.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        self.label_ports.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_ports.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        self.button_scan.grid(row=2, column=0, columnspan=2, pady=10)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def scan(self):
        target = self.entry_target.get()
        ports = self.entry_ports.get()

        # Input validation
        if not target or not ports:
            self.display_result("Please enter both target IP and ports.")
            return

        try:
            # Create an Nmap scanner object
            scanner = nmap.PortScanner()

            # Perform the port scan
            scanner.scan(target, ports)

            # Display the results in the text widget
            self.display_result("\nScan Results:\n")
            for host in scanner.all_hosts():
                self.display_result(f"Results for {host}:\n")
                for proto in scanner[host].all_protocols():
                    self.display_result(f"Protocol: {proto}\n")
                    ports = scanner[host][proto].keys()
                    for port in ports:
                        state = scanner[host][proto][port]['state']
                        self.display_result(f"Port {port}: {state}\n")
                self.display_result("\n")
        except nmap.nmap.PortScannerError as e:
            self.display_result(f"Error: {e}")

    def display_result(self, text):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = NetworkScannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

