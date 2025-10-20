from playwright.async_api import async_playwright
import asyncio
from playwright_stealth import Stealth
from data_conversion import excel

baseurl = "https://summerofcode.withgoogle.com"
data = []

async def Scraper():
    clicks = 1

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        stealth = Stealth()
        await stealth.apply_stealth_async(page)

        await page.goto("https://summerofcode.withgoogle.com/programs/2025/projects")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_selector("input[placeholder='Search projects']")
  
        await page.fill("input[placeholder='Search projects']", "Machine Learning")
        await page.wait_for_load_state("networkidle")
        while True:
            buttons = await page.locator('a.mdc-button:has-text("View project details")').all()
            for button in buttons:
                href = await button.get_attribute('href')
                await page.goto(f"{baseurl}{href}")
                await page.wait_for_load_state("networkidle")
                await page.wait_for_selector("div.h-list__item")
                org =  page.locator("div.h-list__item").nth(2)
                orgnization_name = await org.inner_text()
                Topics = page.locator("div.h-list__item").nth(3)
                Topics_name = await Topics.inner_text()
                Technologies  = page.locator("div.h-list__item").nth(4)
                Tech_name = await Technologies.inner_text()
                data.append({"Organization": orgnization_name[12:].strip(),
                "Technologies": Topics_name[12:].strip(),
                "Topics": Tech_name[6:].strip()})
                await page.go_back()
                await page.wait_for_load_state("networkidle")

            next_page = page.locator('button.mat-mdc-paginator-navigation-next').nth(0)
            await page.fill("input[placeholder='Search projects']", "Machine Learning")

            for i in range(clicks):
                  
             if clicks <= 5:
                await next_page.click()
                await page.wait_for_load_state("networkidle")
             else:
                break   
  
            
            clicks += 1
            if clicks > 5:
                break

        await browser.close()
            
    

if __name__ == "__main__":
    asyncio.run(Scraper())
    excel(data)

