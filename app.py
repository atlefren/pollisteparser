#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app import app

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
