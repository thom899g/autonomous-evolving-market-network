"""
Market simulation engine with realistic price generation and order matching
Handles multiple trading pairs with configurable volatility and spreads
"""

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import logging
from dataclasses import dataclass
from collections import defaultdict
import json

logger = logging.getLogger(__name__)

@dataclass
class Order:
    """Order representation for simulation"""
    order_id: str
    symbol: str
    side: str  # 'buy' or '