#!/usr/bin/env python3
import argparse
import os
import subprocess
import shutil
from urllib.parse import urlparse, urljoin
from datetime import datetime
from readability import Document
import requests
from bs4 import BeautifulSoup
import re

def download_site(wayback_url, output_dir="web4_contract/res"):
    """Download website content from Wayback Machine and convert to reader view"""
    if not wayback_url.startswith('https://web.archive.org/web/'):
        raise ValueError("Please provide a full Wayback Machine URL")
    
    # Clean output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    timestamp = wayback_url.split('/web/')[1].split('/')[0]
    timestamp_date = datetime.strptime(timestamp[:8], '%Y%m%d').strftime('%B %d, %Y')
    
    # Download the main page
    response = requests.get(wayback_url, headers={'User-Agent': 'Mozilla/5.0'})
    response.encoding = 'utf-8'  # Explicitly set encoding
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove Wayback Machine elements
    for element in soup.select('#wm-ipp-base, #donato, #wm-ipp-inside, #wm-ipp, #wm-ipp-print'):
        if element:
            element.decompose()
            
    # Remove all script tags
    for script in soup.find_all('script'):
        script.decompose()
        
    # Remove all style tags
    for style in soup.find_all('style'):
        style.decompose()
        
    # Get the title and dates
    title = soup.title.string if soup.title else "Archived Page"
    title = title.replace("â", "'")  # Fix apostrophes
    clean_title = re.sub(r'\s*[|:-]\s*.*$', '', title)  # Remove everything after |, :, or -
    
    today_date = datetime.now().strftime('%B %d, %Y')
    
    # Find the main content
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
    if not main_content:
        main_content = soup.find('body')
    
    # Clean up the content
    if main_content:
        # Fix character encoding
        content_str = str(main_content)
        content_str = content_str.replace("â", "'")
        content_str = content_str.replace("â", '"')
        content_str = content_str.replace("â", '"')
        content_str = content_str.replace("â¦", "...")
        main_content = BeautifulSoup(content_str, 'html.parser')
    
    # Create reader-friendly template
    template = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
                line-height: 1.6;
                max-width: 780px;
                margin: 0 auto;
                padding: 20px;
                color: #2c3e50;
                background-color: #f9f9f9;
            }}
            .banner {{
                background-color: #f8f9fa;
                padding: 15px;
                text-align: center;
                border-radius: 8px;
                margin-bottom: 30px;
                border: 1px solid #dee2e6;
                font-size: 0.9em;
                color: #666;
                position: sticky;
                top: 0;
                z-index: 1000;
                backdrop-filter: blur(10px);
            }}
            .banner-title {{
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 5px;
            }}
            .banner-info {{
                margin-bottom: 3px;
            }}
            .content {{
                background-color: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: #34495e;
                line-height: 1.3;
                margin-top: 1.5em;
                margin-bottom: 0.8em;
            }}
            h1 {{
                font-size: 2.2em;
                margin-top: 0;
                padding-bottom: 0.5em;
                border-bottom: 2px solid #eee;
            }}
            p {{
                margin-bottom: 1.5em;
            }}
            img {{
                max-width: 100%;
                height: auto;
                display: block;
                margin: 2em auto;
                border-radius: 4px;
            }}
            ul, ol {{
                margin: 1em 0;
                padding-left: 2em;
            }}
            li {{
                margin-bottom: 0.5em;
            }}
            blockquote {{
                margin: 2em 0;
                padding: 1em 2em;
                border-left: 4px solid #0051C3;
                background-color: #f8f9fa;
                font-style: italic;
            }}
            code {{
                background-color: #f8f9fa;
                padding: 0.2em 0.4em;
                border-radius: 3px;
                font-family: Consolas, Monaco, 'Andale Mono', monospace;
                font-size: 0.9em;
            }}
            pre {{
                background-color: #f8f9fa;
                padding: 1em;
                border-radius: 8px;
                overflow-x: auto;
            }}
            a {{
                color: #0051C3;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 2em 0;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #dee2e6;
            }}
            th {{
                background-color: #f8f9fa;
                font-weight: 600;
            }}
            .nav-section {{
                margin-bottom: 2em;
                padding: 1em;
                background-color: #f8f9fa;
                border-radius: 8px;
            }}
            .nav-section h2 {{
                margin-top: 0;
            }}
            @media (max-width: 780px) {{
                body {{
                    padding: 15px;
                }}
                .content {{
                    padding: 20px;
                }}
            }}
            
            /* Accordion Styles */
            details.rr-accordion {{
                margin-bottom: 1em;
            }}
            
            details.rr-accordion summary {{
                list-style: none;
                cursor: pointer;
                padding: 1em;
                background-color: #f8f9fa;
                border-radius: 8px;
                position: relative;
            }}
            
            details.rr-accordion summary::-webkit-details-marker {{
                display: none;
            }}
            
            details.rr-accordion summary::after {{
                content: "▼";
                position: absolute;
                right: 1em;
                top: 50%;
                transform: translateY(-50%);
                transition: transform 0.2s;
            }}
            
            details.rr-accordion[open] summary::after {{
                transform: translateY(-50%) rotate(180deg);
            }}
            
            .rr-accordion__title {{
                padding-right: 2em;  /* Make room for the arrow */
                display: inline-block;
                font-weight: 500;
            }}
            
            details.rr-accordion > div {{
                padding: 1em;
                margin-top: 0.5em;
            }}
        </style>
    </head>
    <body>
        <div class="banner">
            <div class="banner-title">{clean_title}</div>
            <div class="banner-info">Archived copy from {timestamp_date} via 
                <a href="{wayback_url}">Wayback Machine</a>
            </div>
            <div class="banner-info">Made unstoppable by <a href="https://github.com/joe-rlo/wayback_web4">web4</a> on {today_date}</div>
        </div>
        <div class="content">
            {str(main_content)}
        </div>
    </body>
    </html>
    '''
    
    # Clean up the content with BeautifulSoup
    final_soup = BeautifulSoup(template, 'html.parser')
    
    # Fix image URLs
    for img in final_soup.find_all('img'):
        if img.get('src'):
            if not img['src'].startswith(('http://', 'https://')):
                img['src'] = urljoin(wayback_url, img['src'])
    
    # Fix links
    for link in final_soup.find_all('a'):
        if link.get('href'):
            if not link['href'].startswith(('http://', 'https://', '#', 'mailto:')):
                link['href'] = urljoin(wayback_url, link['href'])
    
    # Save the transformed content
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(str(final_soup.prettify()))
    
    print(f"Created reader-friendly version of the content from {timestamp_date}")
    return timestamp_date

def build_and_deploy_contract(wallet_name=None, update=False):
    """Build and deploy the Web4 contract"""
    contract_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web4_contract")
    
    # Build the contract
    print("Building Web4 contract...")
    subprocess.run(
        ["cargo", "build", "--target", "wasm32-unknown-unknown", "--release"],
        cwd=contract_dir,
        check=True
    )
    
    wasm_file = os.path.join(contract_dir, "target/wasm32-unknown-unknown/release/wayback_web4.wasm")
    
    if not wallet_name:
        raise ValueError("Wallet name is required for deployment")
    
    # Deploy the contract
    deploy_command = [
        "near", "contract", "deploy",
        wallet_name,
        "use-file", wasm_file,
        "without-init-call",
        "network-config", "mainnet",
        "sign-with-keychain",
        "send"
    ]
    print(f"Updating contract on {wallet_name}...")
    
    subprocess.run(deploy_command, check=True)
    
    return wallet_name

def main():
    parser = argparse.ArgumentParser(description="Wayback Web4 Deployment Tool")
    parser.add_argument("url", help="URL of the site to download from Wayback Machine")
    parser.add_argument("--wallet", help="Existing NEAR wallet to use for deployment")
    parser.add_argument("--update", action="store_true", help="Update existing Web4 deployment")
    
    args = parser.parse_args()
    
    try:
        # Download and transform site
        print("Downloading and transforming site...")
        snapshot_date = download_site(args.url)
        print("Transform complete!")
        
        # Build and deploy
        wallet_name = build_and_deploy_contract(args.wallet, args.update)
        print(f"Site {'updated' if args.update else 'deployed'} successfully!")
        print(f"Your site is available at: https://{wallet_name}.page")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main() 