# OnePlus KernelSU SUSFS — Kernel Improvement Roadmap

> Last updated: 2026-02-26

---

## 1. 🦀 Rust Kernel Support

**Current state:** Rust toolchain detection exists in `action.yml` (line 437) but most builds print `"No RUST toolchain found! Ignoring"`.

**Improvements:**
- Enable proper Rust toolchain for android14-6.1 and android15-6.6 kernels.
- Build Rust-based kernel modules (e.g., Rust binder driver) for better memory safety.
- Add `rust_build: true` for SM8550 / SM8650 / MT6991 devices that support it.
- Consider using the prebuilt Rust toolchain bundled in kernel source (`prebuilts/rust/`).

---

## 2. ⚡ LTO (Link-Time Optimization) Tuning

**Current state:** Workflow supports `lto: none | thin | full`. Most devices likely use `thin`.

**Improvements:**
- Switch flagship Snapdragon devices (SM8550, SM8650) to `lto: full` for max runtime performance.
- Keep MediaTek devices on `thin` LTO due to longer build times.
- Benchmark `full` vs `thin` using kernel boot time and AnTuTu scores.

---

## 3. 🔧 Compiler Optimization Level (O2 vs O3)

**Current state:** Supports `optimize_level: O2 | O3` globally per build.

**Improvements:**
- Use **O3** for Snapdragon 8 Gen 2 (SM8550) and Gen 3 (SM8650) — benefits gaming and heavy workloads.
- Use **O3** + `-fprofile-use` (PGO) if build infra supports profile-guided optimization.
- Use **O2** for MediaTek devices to avoid potential compiler bugs with aggressive unrolling.

---

## 4. 🌐 Networking Improvements

### TCP Congestion Control
- **BBR3:** Upgrade from BBR/BBRv1 to BBRv3 (latest from Google) for better throughput and fairness.
- **CUBIC fallback:** Ensure CUBIC is still available as a safe fallback.

### Queue Discipline
- **CAKE:** Add CAKE (`sch_cake`) as a qdisc option for smarter traffic shaping — beneficial for hotspot users.
- **FQ-CoDel:** Enable `net.core.default_qdisc=fq_codel` by default.

### Other
- **ECN (Explicit Congestion Notification):** Enable ECN support for lower latency on capable networks.
- **TCP Fast Open:** Enable by default for faster connection establishment.
- **MPTCP:** Experimental — add Multipath TCP for redundant network paths.

---

## 5. 🧠 Memory Management

- **ZRAM + Zstd:** Set ZRAM compression algorithm to `zstd` (faster than lz4 in benchmarks) and tune size.
- **ZSWAP:** Consider enabling ZSWAP as an alternative/complement to ZRAM.
- **Memory pressure tuning:** Tune `vm.swappiness`, `vm.dirty_ratio`, `vm.dirty_background_ratio` via init scripts in AnyKernel3.
- **OOM Killer tuning:** Improve OOM score adjustments for better app retention under memory pressure.

---

## 6. 🖥️ CPU / Scheduler Improvements

- **HMBIRD Scheduler:** Already enabled (`hmbird: true`) — ensure it's tuned per SoC for best latency.
- **walt_scale_demand_divisor:** Tune WALT scheduler parameters for flagship SoCs.
- **schedutil governor:** Confirm schedutil is used over userspace/performance for daily use.
- **EAS (Energy Aware Scheduling):** Validate EAS is working correctly on big.LITTLE SoC configs.
- **Latency-Nice support:** Add latency-nice CPU priority for UI threads.

---

## 7. 🔋 Power / Battery Efficiency

- **Power-efficient workqueue:** Enable `CONFIG_WQ_POWER_EFFICIENT_DEFAULT=y`.
- **Wifi scan power saving:** Enable power-efficient WiFi background scan.
- **Suspend tuning:** Tune `wakeup_interval` and deep idle governors per SoC.
- **cpuidle tuning:** Enable deeper C-states on idle to save battery.
- **devfreq tuning:** Review and tune GPU/DDR devfreq governor parameters.

---

## 8. 🔐 Security Enhancements

- **KernelSU Next updates:** Track and integrate latest KernelSU-Next commits promptly.
- **SUSFS updates:** Monitor simonpunk/susfs4ksu for new branches and update `DEFAULT_SUSFS` map in `action.yml`.
- **SELinux permissive toggle:** Optionally expose a toggle (already handled by KernelSU).
- **Kernel address sanitizer (KASAN):** Optional debug build with KASAN enabled for security testing.
- **Stack protector strong:** Ensure `CONFIG_STACKPROTECTOR_STRONG=y` is set across all targets.

---

## 9. 📡 VPN & Tunneling

- **WireGuard built-in:** Ensure WireGuard is compiled as built-in (not module) for kernel-native VPN.
- **WireGuard performance:** Test latency/throughput improvements over OpenVPN.
- **TUN/TAP:** Confirm TUN/TAP module is included for OpenVPN compatibility.

---

## 10. 📦 New Device Support

| Device | SoC | Android | Status |
|---|---|---|---|
| OnePlus 13 | SM8750 (Snapdragon 8 Elite) | android15 | 🔜 Add when kernel source released |
| OnePlus Nord 4 | SM7675 | android14 | 🔜 Pending kernel_manifest branch |
| OnePlus Pad 2 | SM8775 | android15 | 🔜 Pending source availability |
| OnePlus 13R | SM7550 | android14 | 🔜 Check OOS source |

---

## 11. 🛠️ Build System & CI/CD Improvements

### Workflow Quality
- **Suppress Rust warning:** For devices without Rust toolchain, silence with `2>/dev/null` or a conditional check.
- **Build summary comment:** Auto-post a release summary (kernel version, KSU version, SUSFS version, build time, ccache hit rate) as a GitHub release description.
- **SUSFS auto-update notifier:** Add a job to check for new SUSFS tags and open a PR/issue automatically.
- **Parallel matrix batching:** Group smaller builds to reduce GitHub Actions concurrency billing.
- **Workflow dispatch defaults:** Improve `workflow_dispatch` input defaults and descriptions for easier manual triggers.

### Cache Optimization
- **Increase ccache size:** Current max is `1G` — consider `2G` for faster incremental builds.
- **Per-SoC cache keys:** Add SoC family to ccache key for better cache hit rates across device variants sharing the same kernel.

### Artifact Management
- **Checksum file:** Include SHA256 checksums file in release artifacts for verifying downloaded ZIPs.
- **Kernel version badge:** Add a README badge showing the latest built kernel version per device.
- **Auto-release changelog:** Generate a changelog in the GitHub release body based on KSU and SUSFS commit messages.

---

## 12. 📱 AnyKernel3 Enhancements

- **Per-device scripts:** Add device-specific `anykernel.sh` that sets model-specific properties.
- **init.d support:** Bundle `/system/etc/init.d` support scripts for applying tweaks on boot.
- **Magisk module ZIP:** Optionally build a Magisk-compatible module format alongside AnyKernel3 ZIP.
- **Version metadata:** Embed kernel version and build date into the ZIP filename automatically.

---

## 13. 📊 Monitoring & Observability

- **Kernel ftrace:** Ensure ftrace is enabled for profiling support.
- **perf tool compatibility:** Build with `CONFIG_PERF_EVENTS=y` for `perf` profiling.
- **Build time tracking:** Already tracked via `build_time` output — add trending chart in README.
- **Compiler warning count:** Already tracked via `warnings` output — add a threshold gate to fail on regression.

---

## Priority Summary

| Priority | Improvement |
|---|---|
| ⭐⭐⭐ High | BBR3 networking, SUSFS auto-update, O3 for flagship SoCs |
| ⭐⭐ Medium | Full LTO for SM8550/SM8650, ZRAM Zstd, New device support |
| ⭐ Low | Rust build support, CAKE qdisc, Magisk module ZIP |
