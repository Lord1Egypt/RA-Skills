#!/usr/bin/env python3
"""
Interactive Card News Generator
Prompts user for title, content, and background color
"""

import sys
from generate_card import create_card_news


def get_multiline_input(prompt):
    """Get multiline input from user"""
    print(prompt)
    print("(여러 줄 입력 가능. 빈 줄을 입력하면 종료)")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)


def get_color_input(prompt, default):
    """Get color input in RGB format"""
    print(prompt)
    print(f"형식: R,G,B (예: 245,243,238 또는 빈 값 입력시 기본값: {default})")
    
    color_input = input(">>> ").strip()
    
    if not color_input:
        return default
    
    try:
        # Parse RGB values
        rgb = [int(x.strip()) for x in color_input.split(',')]
        
        if len(rgb) != 3:
            print("⚠️  RGB 값은 3개여야 합니다. 기본값을 사용합니다.")
            return default
        
        # Validate range
        for val in rgb:
            if not (0 <= val <= 255):
                print("⚠️  RGB 값은 0-255 범위여야 합니다. 기본값을 사용합니다.")
                return default
        
        # Convert to hex
        hex_color = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
        print(f"✓ 선택된 색상: {hex_color}")
        return hex_color
        
    except ValueError:
        print("⚠️  올바른 형식이 아닙니다. 기본값을 사용합니다.")
        return default


def main():
    print("=" * 50)
    print("  📱 카드 뉴스 생성기")
    print("=" * 50)
    print()
    
    # Get title
    print("1️⃣  제목을 입력하세요")
    print("   (줄바꿈하려면 Enter를 누르고 계속 입력)")
    title = get_multiline_input("")
    
    if not title:
        print("❌ 제목은 필수입니다.")
        sys.exit(1)
    
    print()
    
    # Get content
    print("2️⃣  본문 내용을 입력하세요")
    content = get_multiline_input("")
    
    if not content:
        print("❌ 내용은 필수입니다.")
        sys.exit(1)
    
    print()
    
    # Get background color
    print("3️⃣  배경색을 선택하세요")
    print("\n추천 색상:")
    print("  • 따뜻한 베이지: 245,243,238")
    print("  • 소프트 핑크: 255,229,229")
    print("  • 민트 그린: 224,244,241")
    print("  • 라벤더: 232,224,245")
    print("  • 피치: 255,232,214")
    print("  • 스카이 블루: 227,242,253")
    print()
    
    bg_color = get_color_input("배경색 RGB", "#F5F3EE")
    
    print()
    
    # Get text color
    print("4️⃣  텍스트 색상을 선택하세요")
    text_color = get_color_input("텍스트 RGB", "#1A1A1A")
    
    print()
    
    # Get number badge (optional)
    print("5️⃣  카드 번호를 입력하세요 (선택사항)")
    print("   (빈 값 입력시 번호 없음)")
    number_input = input(">>> ").strip()
    
    number = None
    if number_input:
        try:
            number = int(number_input)
            print(f"✓ 번호: {number}")
        except ValueError:
            print("⚠️  올바른 숫자가 아닙니다. 번호 없이 생성합니다.")
    
    print()
    
    # Get output filename
    print("6️⃣  저장할 파일명을 입력하세요")
    print("   (예: card_01.png)")
    filename = input(">>> ").strip()
    
    if not filename:
        filename = "card.png"
    
    if not filename.endswith('.png'):
        filename += '.png'
    
    output_path = f"/mnt/user-data/outputs/{filename}"
    
    print()
    print("=" * 50)
    print("🎨 카드 생성 중...")
    print("=" * 50)
    
    # Generate card
    try:
        create_card_news(
            title=title,
            content=content,
            output_path=output_path,
            bg_color=bg_color,
            text_color=text_color,
            number=number
        )
        print()
        print("✅ 완료!")
        print(f"📁 저장 위치: {output_path}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
