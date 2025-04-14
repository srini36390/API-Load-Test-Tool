import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import threading
import time
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_test():
    url = url_entry.get()
    headers_str = headers_entry.get()
    body_str = body_entry.get()
    num_requests_str = num_requests_entry.get()

    try:
        num_requests = int(num_requests_str)
        headers = json.loads(headers_str) if headers_str else {}
        body = json.loads(body_str) if body_str else None

    except ValueError:
        messagebox.showerror("Error", "Invalid input for number of requests.")
        return
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON format for headers or body.")
        return

    results_text.delete(1.0, tk.END)
    results = []
    threads = []
    pass_count = 0
    total_time = 0
    response_times = []
    request_numbers = []
    error_counts = {}
    error_messages = {} # Dictionary to store error messages

    def make_request(url, headers, body, results, request_num):
        nonlocal pass_count, total_time, response_times, request_numbers, error_counts, error_messages
        try:
            start_time = time.time()
            if body:
                response = requests.post(url, headers=headers, json=body)
            else:
                response = requests.get(url, headers=headers)
            end_time = time.time()
            response_time = end_time - start_time
            results.append((response.status_code, response_time, response.text))
            if response.status_code == 200:
                pass_count += 1
            else:
                error_counts[response.status_code] = error_counts.get(response.status_code, 0) + 1
                error_messages[response.status_code] = error_messages.get(response.status_code, "") + f"Request {request_num}: {response.text[:100]}...\n" #store first 100 characters of response
            total_time += response_time
            response_times.append(response_time)
            request_numbers.append(request_num)
        except requests.exceptions.RequestException as e:
            results.append((str(e), 0, ""))
            response_times.append(0)
            request_numbers.append(request_num)
            error_counts["Request Exception"] = error_counts.get("Request Exception", 0) + 1
            error_messages["Request Exception"] = error_messages.get("Request Exception", "") + f"Request {request_num}: {str(e)}\n"

    for i in range(num_requests):
        thread = threading.Thread(target=make_request, args=(url, headers, body, results, i + 1))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if num_requests > 0:
        avg_response_time = total_time / num_requests
        pass_percentage = (pass_count / num_requests) * 100
    else:
        avg_response_time = 0
        pass_percentage = 0

    results_text.insert(tk.END, f"Total Requests: {num_requests}\n")
    results_text.insert(tk.END, f"Average Response Time: {avg_response_time:.4f} seconds\n")
    results_text.insert(tk.END, f"Pass Percentage (200 Status): {pass_percentage:.2f}%\n\n")

    if error_counts:
        results_text.insert(tk.END, "Error Counts:\n")
        for error_code, count in error_counts.items():
            results_text.insert(tk.END, f"{error_code}: {count}\n")
            if error_code in error_messages:
                results_text.insert(tk.END,f"Error Messages ({error_code}):\n{error_messages[error_code]}\n")
        results_text.insert(tk.END, "\n")

    log_data = f"Load Test Results - {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    log_data += f"URL: {url}\n"
    log_data += f"Headers: {headers}\n"
    log_data += f"Body: {body}\n"
    log_data += f"Total Requests: {num_requests}\n"
    log_data += f"Average Response Time: {avg_response_time:.4f} seconds\n"
    log_data += f"Pass Percentage (200 Status): {pass_percentage:.2f}%\n\n"
    for status, response_time, text in results:
        log_data += f"Status: {status}, Response Time: {response_time:.4f} seconds\n"
        log_data += f"Response Text: {text[:200]}...\n\n"
    if error_counts:
        log_data += "Error Counts:\n"
        for error_code, count in error_counts.items():
            log_data += f"{error_code}: {count}\n"
            if error_code in error_messages:
                log_data+=f"Error Messages ({error_code}):\n{error_messages[error_code]}\n"

    with open("load_test_results.txt", "w") as f:
        f.write(log_data)

    results_text.insert(tk.END, "Response details logged to load_test_results.txt\n")

    # Graph plotting
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(request_numbers, response_times)
    ax.set_xlabel("Request Number")
    ax.set_ylabel("Response Time (seconds)")
    ax.set_title("Response Time vs. Request Number")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    global canvas_widget
    canvas_widget = canvas.get_tk_widget()

def refresh_test():
    global canvas_widget
    if canvas_widget:
        canvas_widget.destroy()
    url_entry.delete(0, tk.END)
    headers_entry.delete(0, tk.END)
    body_entry.delete(0, tk.END)
    num_requests_entry.delete(0, tk.END)
    results_text.delete(1.0, tk.END)

# UI Setup
root = tk.Tk()
root.title("Load Test Application")

url_label = tk.Label(root, text="URL:")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

headers_label = tk.Label(root, text="Headers (JSON):")
headers_label.pack()
headers_entry = tk.Entry(root, width=50)
headers_entry.pack()

body_label = tk.Label(root, text="Body (JSON):")
body_label.pack()
body_entry = tk.Entry(root, width=50)
body_entry.pack()

num_requests_label = tk.Label(root, text="Number of Concurrent Requests:")
num_requests_label.pack()
num_requests_entry = tk.Entry(root, width=10)
num_requests_entry.pack()

run_button = tk.Button(root, text="Run Load Test", command=load_test)
run_button.pack()

refresh_button = tk.Button(root, text="Refresh Test", command=refresh_test)
refresh_button.pack()

results_text = scrolledtext.ScrolledText(root, width=80, height=10)
results_text.pack()

global canvas_widget
canvas_widget = None

root.mainloop()