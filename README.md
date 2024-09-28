# RSS Link Management Tool

This project provides a simple way to manage and validate RSS links, and convert them to OPML format.

![](/images/success.png)

English | [简体中文](./README.zh-CN.md)

## Features

- Store and manage RSS links
- Validate RSS link effectiveness
- Convert RSS links to OPML format

## Usage

1. Fork this project to your GitHub account.

2. Edit the `rss_links.csv` file:
    - Add new RSS links
    - Specify categories and names for each link

3. Run the `sensing.py` script to validate the RSS links:
    - python sensing.py
    - Note: The current validation accuracy may need further improvement.

4. Use the `convert.py` script to convert the CSV file to OPML format:
    - python convert.py


## File Descriptions

-  `rss_links.csv`: CSV file storing RSS links and their related information
- `sensing.py`: Python script for validating RSS link effectiveness
- `convert.py`: Python script for converting CSV file to OPML format

## Contributing

Issue reports and improvement suggestions are welcome. If you want to contribute code, please fork this project and submit a pull request.