import pytest
from playwright.sync_api import expect
from tests.pages.browserstack_demo_page import BrowserStackDemoPage, SmartphoneBrand

# Firstly, let's create a fixture that will be used to start each test on the BrowserStack demo ecommerce page.
@pytest.fixture(scope="function")
def browserstack_demo_page(page):
    """Start each test on the BrowserStack demo ecommerce page."""
    demo_page = BrowserStackDemoPage(page)
    demo_page.navigate()
    return demo_page

@pytest.fixture(scope="module")
def smartphone_brand():
    """Fixture to get a smartphone brand."""
    return SmartphoneBrand

# Now, let's create a test class for the BrowserStack demo ecommerce page.
class TestBstackDemo:
    """Test the BrowserStack demo ecommerce page."""

    def test_navigation(self, browserstack_demo_page):
        """Test that the BrowserStack demo ecommerce page can be navigated to."""
        # Expect the page to have the correct title.
        expect(browserstack_demo_page.page).to_have_title("StackDemo")

    def test_count_products(self, browserstack_demo_page):
        """Test that the BrowserStack demo ecommerce page has the correct number of products."""
        # Expect the page to have 25 products.
        expect(browserstack_demo_page.product_count).to_have_text("25 Product(s) found.")

        expect(browserstack_demo_page.products).to_have_count(25)

    @pytest.mark.parametrize(
        "brand, count",
        (
            (SmartphoneBrand.APPLE, 9),
            (SmartphoneBrand.SAMSUNG, 7),
            (SmartphoneBrand.GOOGLE, 3),
            (SmartphoneBrand.ONEPLUS, 6),
        )
    )
    def test_filter_by_brand(self, browserstack_demo_page, brand, count):
        """Test that the BrowserStack demo ecommerce page can be filtered by brand."""
        # Expect the page to have 25 products initially.
        expect(browserstack_demo_page.product_count).to_have_text("25 Product(s) found.")

        # Filter by brand "Samsung".
        browserstack_demo_page.filter_by_brand(brand)

        # Expect the page to have 5 products.
        expect(browserstack_demo_page.product_count).to_have_text(f"{count} Product(s) found.")
