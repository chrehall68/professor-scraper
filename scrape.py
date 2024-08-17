import playwright.async_api as pw
import asyncio
import argparse
import bs4


async def scrape(url: str, class_: str) -> bs4.BeautifulSoup:
    async with pw.async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        print("loading class schedules...")
        await page.get_by_role("button", name="Load Class Schedule").click()

        # now, use the search bar
        print("entering search...")
        await page.get_by_label("Search:").fill(class_)

        print("setting number of results to 100...")
        await page.get_by_label("Show ").select_option("100")

        # finally, capture inner html
        html = await page.inner_html("body")

        await browser.close()

    # parse html and capture data
    return bs4.BeautifulSoup(html, "html.parser")


async def get_profs(soup: bs4.BeautifulSoup, class_: str, types: list[str]) -> set:
    # first, go to the correct table:
    r = soup.find_all(attrs={"id": "classSchedule"})
    assert len(r) == 1
    r = r[0]

    profs = set()

    for row in r.find_all("tr"):
        # take the 10th column
        tds = row.find_all("td")
        if len(tds) == 14:
            class_id = tds[0].text
            if class_ + " " in class_id:
                prof_name = tds[9].text
                try:
                    email = tds[9].find_all("a")[0]["href"].replace("mailto:", "")
                except:
                    print("no email found for", tds[9])
                t = tds[6].text
                if t.strip() in types:
                    profs.add((prof_name, email))

    return profs


async def main(url: str, class_: str, types: list[str]) -> None:
    soup = await scrape(url, class_)
    profs = await get_profs(soup, class_, types)
    print(profs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str)
    parser.add_argument("class_", type=str)
    parser.add_argument("--types", nargs="+", type=str, default=["LEC", "LAB", "SEM"])
    args = parser.parse_args()
    asyncio.run(main(args.url, args.class_, args.types))
