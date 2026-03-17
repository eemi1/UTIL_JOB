
from playwright.async_api import async_playwright

async def scrape_restaurants(input: str):

    data = []

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        query = input.replace(" ", "+")
        url = f"https://www.google.com/maps/search/{query}"
        await page.goto(url)

        await page.wait_for_selector(".Nv2PK")

        restaurants = await page.query_selector_all(".Nv2PK")

        for r in restaurants[:10]:

            name_el = await r.query_selector(".qBF1Pd")
            name = await name_el.inner_text()

            await r.click()
            await page.wait_for_timeout(2000)

            phone = None
            website = None

            try:
                phone_link = await page.wait_for_selector('a[href^="tel:"]', timeout=3000)
                phone = await phone_link.get_attribute("href")
                phone = phone.replace("tel:", "")
            except:
                pass

            web_el = await page.query_selector('a[data-item-id="authority"]')
            if web_el:
                website = await web_el.get_attribute("href")

            data.append({
                "name": name,
                "phone": phone,
                "website": website
            })

        await browser.close()

    return data