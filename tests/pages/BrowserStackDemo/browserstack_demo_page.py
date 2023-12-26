from enum import Enum

from playwright.sync_api import Page

class SmartphoneBrand(Enum):
    """Enum for smartphone brands."""
    APPLE = "Apple"
    SAMSUNG = "Samsung"
    GOOGLE = "Google"
    ONEPLUS = "OnePlus"

class BrowserStackDemoPage():
    """
    Page model for the BrowserSatck demo ecommerce page.
    
    The page is composed by a grid of products that can be added to a cart, filtered by brand and sorted.
    """

    def __init__(self, page: Page) -> None:
        """Constructor for the BrowserStackDemoPage class."""
        self.page = page
        self.product_count = self.page.get_by_text("Product(s) found")

    def navigate(self):
        """Navigate to the BrowserStack demo ecommerce page."""
        self.page.goto("https://bstackdemo.com/")

    @property
    def products(self):
        """Get all products."""
        return self.page.locator("div.shelf-item")

    def filter_by_brand(self, brand: SmartphoneBrand):
        """
        Filter products by brand.

        Args:
            brand (SmartphoneBrand): The brand to filter by.
        """
        self.page.locator("span.checkmark").filter(has_text=brand.value).click()
