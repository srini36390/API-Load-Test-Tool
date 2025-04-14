# API Load Testing Tool (Python/Tkinter)

This Python application provides a basic, easy-to-use graphical interface for load testing APIs. It allows you to simulate concurrent requests, analyze performance metrics, and identify potential bottlenecks.

## Features

* **API Load Testing:** Simulates concurrent requests to a specified API endpoint (GET/POST).
* **Performance Metrics:** Calculates and displays average response time, pass percentage (200 status codes), and error counts.
* **Concurrency Control:** Configurable number of concurrent requests.
* **JSON Input:** Supports HTTP headers and request bodies in JSON format.
* **Response Time Graph:** Visualizes response times using `matplotlib`.
* **Error Reporting:** Displays HTTP error codes and messages.
* **Detailed Logging:** Logs test results to `load_test_results.txt`.
* **Simple UI:** Uses `tkinter` for a straightforward graphical interface.
* **Refresh Button:** Clears input and results for a new test.

## Usage

1.  Clone the repository.
2.  Run the Python script.
3.  Enter the API URL, headers, body (if needed), and the number of concurrent requests.
4.  Click "Run Load Test".
5.  Analyze the results in the text box and the generated graph.
6.  Click "Refresh Test" to start a new test.

## Dependencies

* `tkinter` (standard Python library)
* `requests`
* `matplotlib`

## Limitations

* Basic functionality compared to dedicated load testing tools.
* Primarily for HTTP-based APIs.
* Limited scripting capabilities.
* Simple UI and graphs.

## Use Cases

* Quickly testing the performance of simple APIs.
* Identifying basic performance bottlenecks.
* Verifying API reliability under moderate load.
* Developer testing during API development.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for bug fixes or enhancements.





