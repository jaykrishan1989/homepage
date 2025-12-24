from playwright.sync_api import sync_playwright
from datetime import datetime
import time

def get_nanaimo_briefing_manual_bypass(icao="CYVR"):
    with sync_playwright() as p:
        # Step 1: Headless=False allows you to solve the CAPTCHA manually
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0")
        page = context.new_page()

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Awaiting Human Verification for {icao}...")
        url = f"https://plan.navcanada.ca/wxrecall/results?locations={icao}&types=notam"
        
        try:
            page.goto(url)
            
            # Step 2: The script waits for YOU to solve the challenge.
            # It will proceed as soon as it sees the results list on the screen.
            print(" >> Action Required: If a 'Verify you are human' box appears, please click it.")
            page.wait_for_selector(".results-list", timeout=120000) # 2 minute window
            
            # Step 3: Extract the data once the human is verified
            time.sleep(2) # Final render buffer
            notams = page.locator(".notam-text, pre").all_text_contents()
            
            print("\n" + "═"*70)
            print(f" CAPTURED BRIEFING: {icao} | {datetime.now().strftime('%H:%M')}")
            print("═"*70)

            if notams:
                for idx, val in enumerate(notams, 1):
                    print(f" [{idx:02}] {val.strip()[:150]}...")
            else:
                print(" [!] Verification passed, but no data found in the container.")
            
        except Exception as e:
            print(f" [X] System Timeout or Fault: {e}")
        
        browser.close()

if __name__ == "__main__":
    get_nanaimo_briefing_manual_bypass("CYVR")