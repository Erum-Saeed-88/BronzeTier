# AI Employee - Bronze Tier

> **Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

This is a **Bronze Tier** implementation of the Personal AI Employee hackathon. It provides the foundational layer for an autonomous AI agent powered by **Claude Code** and **Obsidian** that proactively manages personal and business affairs.

## Bronze Tier Deliverables ✅

- [x] Obsidian vault with `Dashboard.md` and `Company_Handbook.md`
- [x] One working Watcher script (File System monitoring)
- [x] Claude Code integration for reading/writing to the vault
- [x] Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`
- [x] Orchestrator to trigger Claude Code processing

## Quick Start

### Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| [Claude Code](https://claude.com/product/claude-code) | Active subscription | Primary reasoning engine |
| [Obsidian](https://obsidian.md/download) | v1.10.6+ | Knowledge base & dashboard |
| [Python](https://www.python.org/downloads/) | 3.13+ | Watcher scripts |
| [Node.js](https://nodejs.org/) | v24+ LTS | MCP servers (future) |

### Installation

1. **Install Python dependencies:**

```bash
cd scripts
pip install watchdog
```

2. **Verify Claude Code is installed:**

```bash
claude --version
```

3. **Open the Vault in Obsidian:**
   - Launch Obsidian
   - Click "Open folder as vault"
   - Select the `Vault` folder in this project

### Running the System

#### Option 1: Manual Processing (Simple)

1. Drop files into `Vault/Inbox/` folder
2. Run Claude Code manually:

```bash
cd Vault
claude "Process all files in /Needs_Action folder. Read each file, determine required actions, and move completed items to /Done."
```

#### Option 2: Automated Watcher + Orchestrator

**Terminal 1 - Start the File System Watcher:**

```bash
cd scripts
python filesystem_watcher.py ../Vault
```

**Terminal 2 - Start the Orchestrator:**

```bash
cd scripts
python orchestrator.py ../Vault
```

**Terminal 3 - Run Claude Code:**

```bash
cd Vault
claude "You are an AI Employee. Check /Needs_Action folder for pending tasks. Process each item according to Company_Handbook.md rules. Move completed items to /Done."
```

## Directory Structure

```
BronzeTier/
├── scripts/
│   ├── base_watcher.py         # Abstract base class for watchers
│   ├── filesystem_watcher.py   # File system monitor (Bronze tier)
│   ├── orchestrator.py         # Triggers Claude Code processing
│   └── requirements.txt        # Python dependencies
├── Vault/                      # Obsidian vault
│   ├── Inbox/                  # Drop folder for new files
│   ├── Needs_Action/           # Pending items for Claude to process
│   ├── Done/                   # Completed items
│   ├── Pending_Approval/       # Awaiting human approval
│   ├── Approved/               # Approved actions ready to execute
│   ├── Plans/                  # Multi-step task plans
│   ├── Logs/                   # Action logs
│   ├── Dashboard.md            # Real-time status dashboard
│   ├── Company_Handbook.md     # Rules of engagement
│   └── Business_Goals.md       # Business objectives
└── README.md                   # This file
```

## How It Works

### Architecture: Perception → Reasoning → Action

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Watchers   │────▶│  Obsidian    │────▶│ Claude Code │
│  (Senses)   │     │  (Memory)    │     │  (Brain)    │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Dashboard  │
                    │   (GUI)      │
                    └──────────────┘
```

### File System Watcher Flow

1. **Drop** a file into `Vault/Inbox/`
2. **Watcher detects** the new file within 1-2 seconds
3. **Copies** file to `Needs_Action/` with metadata `.md` file
4. **Orchestrator** detects pending items and creates Claude prompt
5. **Claude Code** processes the item and moves to `Done/`

### Example: Processing a File Drop

```bash
# 1. Copy a file to Inbox
cp document.pdf Vault/Inbox/

# 2. Watcher automatically creates:
#    - Vault/Needs_Action/FILE_20260228_120000_document.pdf
#    - Vault/Needs_Action/FILE_20260228_120000_document.pdf.md

# 3. Run Claude Code to process
cd Vault
claude "Process the new file drop in Needs_Action"

# 4. Claude reviews, takes action, moves to Done
```

## Usage Patterns

### Pattern 1: File Drop Processing

Drop any file into `/Inbox/` for AI processing:
- Documents to summarize
- Emails to reply to
- Invoices to process
- Tasks to plan

### Pattern 2: Manual Task Creation

Create a `.md` file directly in `/Needs_Action/`:

```markdown
---
type: task
priority: high
created: 2026-02-28
---

# Task: Review Q1 Budget

Please review the budget spreadsheet and identify:
1. Overspent categories
2. Cost saving opportunities
3. Recommendations for Q2
```

### Pattern 3: Approval Workflow

For sensitive actions:

1. Claude creates: `/Pending_Approval/PAYMENT_Client_A.md`
2. User reviews and moves to `/Approved/`
3. Claude executes the action
4. Result logged to `/Logs/`

## Configuration

### Company Handbook

Edit `Vault/Company_Handbook.md` to customize:
- Communication guidelines
- Payment thresholds
- Task prioritization rules
- Approval requirements

### Business Goals

Edit `Vault/Business_Goals.md` to set:
- Revenue targets
- Key metrics
- Active projects
- Subscription audit rules

## Testing

### Test the File System Watcher

1. Start the watcher:

```bash
cd scripts
python filesystem_watcher.py ../Vault
```

2. Copy the test file:

```bash
cp Vault/Inbox/test_document.txt Vault/Inbox/test2.txt
```

3. Verify output:
   - Check `Vault/Needs_Action/` for new files
   - Metadata `.md` file should be created

### Test Claude Code Integration

```bash
cd Vault
claude "Read Company_Handbook.md and summarize the key rules"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Watcher not detecting files | Ensure watcher is running; check folder permissions |
| Claude Code not found | Run `npm install -g @anthropic/claude-code` |
| Files not moving to Done | Claude may need explicit instruction to move files |
| Import errors in Python | Run `pip install watchdog` |

## Next Steps (Silver Tier)

To upgrade to Silver Tier:
- [ ] Add Gmail Watcher (requires Gmail API setup)
- [ ] Add WhatsApp Watcher (requires Playwright)
- [ ] Implement MCP server for sending emails
- [ ] Create human-in-the-loop approval workflow
- [ ] Add scheduled tasks via cron/Task Scheduler

## Security Notes

⚠️ **Important Security Practices:**

1. **Never commit credentials** - Add `.env` files to `.gitignore`
2. **Use environment variables** for API keys
3. **Review before approving** - Always check approval requests
4. **Audit logs regularly** - Check `/Logs/` for unexpected actions

## Resources

- [Full Hackathon Blueprint](./Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Claude Code Documentation](https://docs.anthropic.com/claude-code/)
- [Obsidian Help](https://help.obsidian.md/)
- [Watchdog Documentation](https://pythonhosted.org/watchdog/)

## License

This project is part of the Personal AI Employee Hackathon. Share and build upon it freely.

---

*Built with ❤️ for the AI Employee Hackathon - Bronze Tier*
