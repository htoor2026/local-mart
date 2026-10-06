from pathlib import Path
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
IMAGE_DIR = ROOT / "docs" / "images"

IMAGE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("Saving screenshots to:")
print(IMAGE_DIR)


def capture_section(
    page,
    title_text,
    filename,
    extra_top=100,
    extra_bottom=700,
):

    # First try finding it as a heading
    locator = page.get_by_role(
        "heading",
        name=title_text,
        exact=False
    )

    # Fallback to any text containing the phrase
    if locator.count() == 0:
        locator = page.get_by_text(
            title_text,
            exact=False
        )

    if locator.count() == 0:
        print(
            f"Could not find section: {title_text}"
        )
        return

    locator = locator.first

    locator.scroll_into_view_if_needed()

    page.wait_for_timeout(700)

    box = locator.bounding_box()

    if not box:
        print(
            f"Could not get position for: {title_text}"
        )
        return

    page_height = page.evaluate(
        "() => document.documentElement.scrollHeight"
    )

    y = max(
        0,
        box["y"] - extra_top
    )

    height = min(
        extra_bottom,
        page_height - y
    )

    page.screenshot(
        path=str(
            IMAGE_DIR / filename
        ),
        clip={
            "x": 0,
            "y": y,
            "width": 1440,
            "height": height,
        }
    )

    print(
        "Saved:",
        filename
    )


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page(
        viewport={
            "width": 1440,
            "height": 1100
        }
    )

    page.goto(
        "http://localhost:8501",
        wait_until="domcontentloaded"
    )

    page.wait_for_timeout(5000)


    # ======================================================
    # BUSINESS VIEW
    # ======================================================

    page.get_by_role(
        "tab",
        name="Business View"
    ).click()

    page.wait_for_timeout(1200)


    capture_section(
        page,
        "profit-aware optimization",
        "strategy-comparison.png",
        extra_top=100,
        extra_bottom=750,
    )


    # 2. Store recommendations
    capture_section(
        page,
        "Store promotion recommendations",
        "store-recommendations.png",
        extra_top=80,
        extra_bottom=900,
    )


    # 3. Strategy comparison
    capture_section(
        page,
        "Why profit-aware optimization matters",
        "strategy-comparison.png",
        extra_top=80,
        extra_bottom=750,
    )


    # ======================================================
    # TECHNICAL BUILD
    # ======================================================

    page.get_by_role(
        "tab",
        name="Technical Build"
    ).click()

    page.wait_for_timeout(1200)


    # 4. Technical architecture
    capture_section(
        page,
        "System architecture",
        "technical-architecture.png",
        extra_top=100,
        extra_bottom=700,
    )


    # 5. Uplift evaluation
    capture_section(
        page,
        "2. Promotion uplift modeling",
        "uplift-evaluation.png",
        extra_top=80,
        extra_bottom=900,
    )


    browser.close()


print("\nAll screenshots completed.")