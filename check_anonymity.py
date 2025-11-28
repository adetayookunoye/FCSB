#!/usr/bin/env python3
"""
AISTAT Anonymity Compliance Checker
Scans notebook for personal directory information and suggests fixes
"""

import json
import sys
import re
from pathlib import Path

def check_notebook_anonymity(notebook_path):
    """Check notebook for anonymity violations"""
    
    print("\n" + "="*80)
    print("AISTAT ANONYMITY COMPLIANCE CHECKER")
    print("="*80 + "\n")
    
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    # Patterns to search for (adjust as needed)
    patterns = [
        (r'/home/[a-zA-Z0-9_-]+/', 'Unix home directory'),
        (r'/Users/[a-zA-Z0-9_-]+/', 'macOS home directory'),
        (r'C:\\Users\\[a-zA-Z0-9_-]+\\', 'Windows home directory'),
        (r'adetayo', 'Personal username'),
        (r'Adetayo', 'Personal name'),
        (r'CSCI Forms', 'Course/context identifier'),
        (r'Cancer Screening', 'Research project identifier'),
    ]
    
    violations = []
    
    # Check all cells
    for cell_idx, cell in enumerate(notebook.get('cells', [])):
        if cell['cell_type'] == 'code':
            source = ''.join(cell.get('source', []))
            
            for pattern, description in patterns:
                matches = re.finditer(pattern, source)
                for match in matches:
                    # Get line number within cell
                    lines_before = source[:match.start()].count('\n')
                    violations.append({
                        'cell': cell_idx + 1,  # 1-indexed
                        'line_in_cell': lines_before + 1,
                        'pattern': pattern,
                        'description': description,
                        'match': match.group(),
                        'context': source[max(0, match.start()-50):match.end()+50]
                    })
        
        # Also check cell outputs (for print statements)
        for output in cell.get('outputs', []):
            if 'text' in output:
                text = ''.join(output['text'])
                for pattern, description in patterns:
                    matches = re.finditer(pattern, text)
                    for match in matches:
                        violations.append({
                            'cell': cell_idx + 1,
                            'output': True,
                            'pattern': pattern,
                            'description': description,
                            'match': match.group(),
                        })
    
    # Report findings
    if violations:
        print(f"⚠️  FOUND {len(violations)} POTENTIAL ANONYMITY VIOLATIONS:\n")
        
        for i, v in enumerate(violations, 1):
            print(f"{i}. Cell #{v['cell']} - {v['description']}")
            print(f"   Pattern: {v['pattern']}")
            print(f"   Match: {v['match']}")
            if 'line_in_cell' in v:
                print(f"   Line in cell: {v['line_in_cell']}")
            if 'output' in v and v['output']:
                print(f"   Location: Cell output (print statement or similar)")
            if 'context' in v:
                context = v['context'].replace('\n', ' ')[:80]
                print(f"   Context: ...{context}...")
            print()
        
        return False
    else:
        print("✅ NO ANONYMITY VIOLATIONS FOUND!\n")
        print("Your notebook appears safe for AISTAT submission.")
        return True

def create_anonymity_report(notebook_path, output_path="ANONYMITY_REPORT.txt"):
    """Generate a detailed report"""
    
    result = check_notebook_anonymity(notebook_path)
    
    with open(output_path, 'w') as f:
        f.write("AISTAT ANONYMITY COMPLIANCE REPORT\n")
        f.write("="*80 + "\n\n")
        f.write(f"Notebook: {notebook_path}\n")
        f.write(f"Status: {'✅ COMPLIANT' if result else '⚠️ VIOLATIONS FOUND'}\n")
        f.write(f"\nRecommendations:\n")
        if not result:
            f.write("1. Replace hardcoded paths with relative paths using Path.cwd()\n")
            f.write("2. Remove full directory paths from print statements\n")
            f.write("3. Use generic output messages\n")
        f.write("4. See ANONYMITY_COMPLIANCE_GUIDE.md for detailed instructions\n")
    
    print(f"\n📋 Report saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_anonymity.py <notebook_path>")
        print("Example: python check_anonymity.py model.ipynb")
        sys.exit(1)
    
    notebook_file = sys.argv[1]
    
    if not Path(notebook_file).exists():
        print(f"❌ Error: {notebook_file} not found")
        sys.exit(1)
    
    success = check_notebook_anonymity(notebook_file)
    create_anonymity_report(notebook_file)
    
    sys.exit(0 if success else 1)
