# WebCrawler_Project
web crawler capable of extracting data from an e-commerce website efficiently

## Overview

This Python script is a web crawler designed to scrape product data from a website. The current implementation targets "https://www.jiomart.com/" and extracts information about products, including URL, name, price, image, and description. The script limits the crawling depth and the number of visited links.

## Prerequisites

- Python 3.x
- Required Python packages
  - requests
  - beautifulsoup4

## Process of gathering data

After a thorough evaluation of various e-commerce websites, JioMart emerged as the optimal choice for data extraction. The script exclusively targets URLs containing product information, filtering out irrelevant pages without product listings.

## What are we gathering?

We're gathering:

- Product's Image URL
- Product Name
- Product Price
- Product Description

We can gather any other information about product as well.

## Process

The script offers configurability by allowing users to set limits on the number of products to scrape. Additionally, a depth parameter provides control over the extent of crawling. For instance:

- Depth 1 covers all pages until "domain/"
- Depth 2 spans pages until "domain/c"
- Depth 3 encompasses pages until "domain/c/product-info"

To obtain comprehensive product details, the script navigates to the product detail pages, streamlining the extraction of additional product data. Upon completion of the scraping process, the gathered information is consolidated into a JSON file for easy reference and analysis.
