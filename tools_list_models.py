import os
import sys
import json

try:
    import google.generativeai as genai
except Exception as e:
    print("IMPORT_ERROR", e)
    sys.exit(3)

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    print("NO_API_KEY: Set GOOGLE_API_KEY or GEMINI_API_KEY in your environment before running this script.")
    sys.exit(2)

try:
    genai.configure(api_key=api_key)
    models = genai.list_models()
except Exception as e:
    print("LIST_ERROR", e)
    sys.exit(4)

out = []
for m in models:
    try:
        # model may be a mapping or an object
        if isinstance(m, dict):
            out.append(m)
        else:
            # best-effort conversion
            d = {}
            for k in dir(m):
                if k.startswith("_"):
                    continue
                try:
                    v = getattr(m, k)
                    if callable(v):
                        continue
                    d[k] = v
                except Exception:
                    d[k] = str(getattr(m, k))
            out.append(d)
    except Exception:
        out.append(str(m))

print(json.dumps(out, indent=2, default=str))
