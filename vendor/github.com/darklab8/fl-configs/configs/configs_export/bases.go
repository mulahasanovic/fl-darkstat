package configs_export

import (
	"github.com/darklab8/fl-configs/configs/configs_mapped/freelancer_mapped/data_mapped/universe_mapped"
	"github.com/darklab8/fl-configs/configs/configs_mapped/freelancer_mapped/infocard_mapped/infocard"
	"github.com/darklab8/fl-configs/configs/conftypes"
	"github.com/darklab8/go-utils/goutils/utils/utils_types"
)

func (e *Exporter) GetBases() []Base {
	results := make([]Base, 0, len(e.configs.Universe_config.Bases))

	commodities_per_base := e.getMarketGoods()

	for _, base := range e.configs.Universe_config.Bases {
		var name string
		if base_infocard, ok := e.configs.Infocards.Infonames[base.StridName.Get()]; ok {
			name = string(base_infocard)
		}

		var system_name infocard.Infoname
		if system, ok := e.configs.Universe_config.SystemMap[universe_mapped.SystemNickname(base.System.Get())]; ok {
			if infoname, ok := e.configs.Infocards.Infonames[system.Strid_name.Get()]; ok {
				system_name = infoname
			}
		}

		var infocard_id int
		var reputation_nickname string
		var pos conftypes.Vector

		if system, ok := e.configs.Systems.SystemsMap[base.System.Get()]; ok {
			for _, system_base := range system.Bases {
				if system_base.IdsName.Get() == base.StridName.Get() {
					infocard_id = system_base.IDsInfo.Get()
					reputation_nickname = system_base.RepNickname.Get()
					pos, _ = system_base.Pos.GetValue()
				}
			}
		}

		var infocard_ids []int = make([]int, 0)

		infocard_ids = append(infocard_ids, infocard_id)

		if infocard_middle_id, exists := e.configs.InfocardmapINI.InfocardMapTable.Map[infocard_id]; exists {
			infocard_ids = append(infocard_ids, infocard_middle_id)
		}

		var factionName string
		if group, exists := e.configs.InitialWorld.GroupsMap[reputation_nickname]; exists {
			infocard_ids = append(infocard_ids, group.IdsInfo.Get())
			if faction_name, exists := e.configs.Infocards.Infonames[group.IdsName.Get()]; exists {
				factionName = string(faction_name)
			}
		}

		var market_goods []MarketGood
		if found_commodities, ok := commodities_per_base[base.Nickname.Get()]; ok {
			market_goods = found_commodities
		}

		var nickname string = base.Nickname.Get()

		e.exportInfocards(InfocardKey(nickname), infocard_ids...)

		base := Base{
			Name:             name,
			Nickname:         nickname,
			FactionName:      factionName,
			System:           string(system_name),
			SystemNickname:   base.System.Get(),
			StridName:        base.StridName.Get(),
			InfocardID:       infocard_id,
			Infocard:         InfocardKey(nickname),
			File:             utils_types.FilePath(base.File.Get()),
			BGCS_base_run_by: base.BGCS_base_run_by.Get(),
			MarketGoods:      market_goods,
			Pos:              pos,
		}

		results = append(results, base)
	}

	return results
}

func FilterToUserfulBases(bases []Base) []Base {
	var useful_bases []Base = make([]Base, 0, len(bases))
	for _, item := range bases {
		if item.Name == "" {
			continue
		}
		useful_bases = append(useful_bases, item)
	}
	return useful_bases
}

type Base struct {
	Name             string
	Nickname         string
	FactionName      string
	System           string
	SystemNickname   string
	StridName        int
	InfocardID       int
	Infocard         InfocardKey
	File             utils_types.FilePath
	BGCS_base_run_by string
	MarketGoods      []MarketGood
	Pos              conftypes.Vector
}
