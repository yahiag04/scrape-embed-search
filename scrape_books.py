import asyncio
from urllib.parse import urljoin
import pandas as pd
from playwright.async_api import async_playwright

BASE_URL = "https://books.toscrape.com/"

async def scrape_books():

    all_books = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await browser.new_page()

        next_page_url = BASE_URL

        while next_page_url is not None:
            print(f"Scraping page: {next_page_url}")
            await page.goto(next_page_url, wait_until="domcontentloaded")

            cards = page.locator("article.product_pod")
            count = await cards.count()
            print(f"Libri trovati: {count}")

            for i in range (count):
                card = cards.nth(i)
                book_data = await extract_book_fields(context, page,card)
                all_books.append(book_data)

            next_button = page.locator("li.next a")
            if await next_button.count()>0:
                rel_next = await next_button.get_attribute("href")
                next_page_url = urljoin(page.url, rel_next)
            else:
                next_page_url = None

        await browser.close()

    df = pd.DataFrame(all_books)
    print("totale libri raccolti: {len(df}")
    if len(df)<1000:
        print("meno di 1000 righe")
    else:
        print("piu di 1000 righe")

    df.to_csv("books.csv", index=False)



async def fetch_category(context, url: str) -> str:
    page = await context.new_page()
    try:
        await page.goto(url, wait_until="domcontentloaded")
        locator = page.locator("ul.breadcrumb li:nth-child(3) a")
        if await locator.count()==0:
            return "UKNOWN"
        category = await locator.text_content()
        if category:
            return category.strip()
        return "UKNOWN"
    finally:
        await page.close()

async def extract_book_fields(context, page, card) ->dict:
    link=card.locator("h3 a")
    title = await link.get_attribute("title")
    if title is None:
        title=""

    rel_url = await link.get_attribute("href")
    if rel_url is None:
        rel_url = ""
    product_page_url = urljoin(BASE_URL, rel_url)

    price_text = await card.locator(".price_color").text_content()
    if price_text is None:
        price = 0.0
    else:
        price = float(price_text.replace("£","").strip())

    rating_class = await card.locator("p.star-rating").get_attribute("class")
    rating_word = rating_class.split()[-1] if rating_class else ""
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }
    rating = rating_map.get(rating_word, 0)

    category = await fetch_category(context, product_page_url)

    return {
        "title": title,
        "category": category,
        "price": price,
        "rating": rating,
        "product_page_url": product_page_url,
    }


if __name__ == "__main__":
    asyncio.run(scrape_books())