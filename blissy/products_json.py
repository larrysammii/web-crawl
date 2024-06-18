import requests
import json
import os


class ShopifyScraper:
    def __init__(self, baseUrl) -> None:
        self.baseUrl = baseUrl

    def download_json(self, page):
        req = requests.get(
            self.baseUrl + f"products.json?limit=250&page={page}", timeout=5
        )
        req.raise_for_status()

        if len(req.json()["products"]) > 0:
            data = req.json()["products"]
            return data
        else:
            raise TypeError(f"Response received but no products found at page {page}.")

    def parse_json(self, json_data):
        products = []
        count = 0
        try:
            if len(json_data) > 0:
                for product in json_data:
                    id = product["id"]
                    title = product["title"]
                    published_at = product["published_at"]
                    product_type = product["product_type"]

                    for variant in product["variants"]:
                        item = {
                            "id": id,
                            "title": title,
                            "product_type": product_type,
                            "variant_id": variant["id"],
                            "variant_title": variant["title"],
                            "weight": variant["grams"],
                            "price": variant["price"],
                            "available": variant["available"],
                            "compared_at_price": variant["compare_at_price"],
                            "option_1": variant["option1"],
                            "option_2": variant["option2"],
                            "option_3": variant["option3"],
                            "sku": variant["sku"],
                            "published_at": published_at,
                            "created_at": variant["created_at"],
                            "updated_at": variant["updated_at"],
                            "requires_shipping": variant["requires_shipping"],
                        }
                        products.append(item)
                        count += 1

            print("Total Products: ", count)
            return products

        except TypeError as e:
            print("No Products found:", e)


def main():
    slip = ShopifyScraper("https://www.slip.com/")
    results = []
    for i in range(1, 10):
        try:
            data = slip.download_json(i)
            results.append(slip.parse_json(data))
        except:  # noqa: E722
            print(f"Scrape Completed. Total {i - 1} page(s) scraped.")
            break

    return results[0]


if __name__ == "__main__":
    data = main()
    file_name = "products.json"
    file_mode = "w" if not os.path.exists(file_name) else "w+"
    with open("products.json", file_mode) as file:
        json.dump(data, file, indent=2)
